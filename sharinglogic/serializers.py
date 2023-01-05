from rest_framework import serializers
from rest_framework_gis import serializers as gisserializers

class SharingUserReqSerializer(serializers.Serializer):
    name=serializers.CharField()
    timing=serializers.DateTimeField()
    latitude = serializers.DecimalField(max_digits=18, decimal_places=15)
    longitude = serializers.DecimalField(max_digits=18, decimal_places=15)
    isToAirport=serializers.BooleanField()

class SharingUserResSerializer(serializers.Serializer):
    name=serializers.CharField()
    timing=serializers.DateTimeField()
    address = serializers.CharField(default=None)
    distance = serializers.SerializerMethodField()

    def get_distance(self, obj):
        unit = self.context['unit']
        return str(obj['distance'])