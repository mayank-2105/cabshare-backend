from django.db import models
from django.contrib.gis.db import models as gismodels
import uuid
# Create your models here.
class UuidPKField(models.UUIDField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('name', 'id')
        kwargs.setdefault('verbose_name', ('Id'))
        kwargs.setdefault('primary_key', True)
        kwargs.setdefault('default', uuid.uuid4)
        kwargs.setdefault('editable', False)
        super().__init__(*args, **kwargs)
        
class SharingUser(models.Model):
    id = UuidPKField()
    name=models.CharField(max_length=255)
    timing = models.DateTimeField()
    address = models.CharField(verbose_name=('Address'),
        max_length=255, null=True, blank=True)
    trip_location = gismodels.PointField(
        srid=4326, null=True, blank=True)
    isToAirport = models.BooleanField()

    class Meta:
        db_table = 'sharing_user'
        verbose_name = ('Sharing User')
        verbose_name_plural = ('Sharing Users')
        ordering = ['name']

    def __str__(self):
        return '%s (%s)' % (self.__class__.__name__, self.name)
