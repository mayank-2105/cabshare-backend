from django.shortcuts import render
import uuid
from collections import defaultdict
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.postgres.aggregates import ArrayAgg, JSONBAgg
from django.db import IntegrityError, transaction, DatabaseError
from django.db.models import Count, Sum, Avg, Min, Max, Func, Q
from django.db.models import F, Case, BooleanField, Value, When
from itertools import chain
from django.db.models import F, FloatField, Case, BooleanField, Value, When
from django.db.models.functions import Concat
from django.utils.translation import ugettext_lazy as _
from django_filters import rest_framework as drf_filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status as http_status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet
# Create your views here.
from .models import SharingUser
from .serializers import SharingUserReqSerializer, SharingUserResSerializer
from datetime import datetime,timedelta
from cabshare.common.custom_exceptions import ValidationException,SuspiciousOperationException
from cabshare.common.renderers import CustomJSONRenderer
from pprint import pprint
class SharingUserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    
    @swagger_auto_schema(
        request_body=SharingUserReqSerializer,
        responses={200: SharingUserResSerializer(many=True)})
    @action(
        methods=['post'],
        detail=False,
        url_path='fetchall',
        renderer_classes=[CustomJSONRenderer])
    def feeder_list(self, request, *args, **kwargs):
        #self.pagination_class = AggregatedLimitOffsetPagination
        serializer_class = SharingUserResSerializer
        req_serializer = SharingUserReqSerializer(data=request.data)

        if req_serializer.is_valid():
            name=req_serializer.validated_data.get('name')
            trip_timing=req_serializer.validated_data.get('timing')
            address=req_serializer.validated_data.get('address')
            latitude = req_serializer.validated_data.get('latitude')
            longitude = req_serializer.validated_data.get('longitude')
            is_to_airport= req_serializer.validated_data.get('isToAirport')
            user_location = Point(float(longitude), float(latitude), srid=4326)

            start_time = trip_timing-timedelta(hours=2)
            end_time = trip_timing+timedelta(hours=2)
            # pprint(start_time)
            # pprint(end_time)
            try:
                queryset = SharingUser.objects.values('name',
                'timing',
                'address'
                ).filter(isToAirport= is_to_airport,
                timing__gte= start_time,
                timing__lte= end_time).annotate(
                    distance=Distance('trip_location', user_location)).order_by(
                    'distance')
                #pprint(queryset)

                sharinguser_obj = SharingUser(
                    id=uuid.uuid4(),
                    name=name,
                    timing=trip_timing,
                    address=address,
                    trip_location = user_location,
                    isToAirport=is_to_airport
                )

                sharinguser_obj.save()

                
                unit = 'km'

                res_serializer = SharingUserResSerializer(queryset, many=True, context={'unit': unit})
                return Response(res_serializer.data, status=http_status.HTTP_200_OK)


            except Exception as e:
                print(e)
                raise SuspiciousOperationException(_('No User found'))

        else:
            raise ValidationException(req_serializer.errors, code=http_status.HTTP_400_BAD_REQUEST)
