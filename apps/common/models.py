from django.db import models
from . import managers


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = managers.Manager()

    class Meta:
        abstract = True


class Region(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'regions'


class Point(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, verbose_name='Longitude')
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, verbose_name='Latitude')
    region = models.ForeignKey(Region, verbose_name="Region", on_delete=models.SET_NULL, null=True)
    deleted = models.BooleanField(default=False, verbose_name="Active")

    active_objects = managers.ActivePointManager()
    objects = models.Manager()

    class Meta:
        db_table = 'points'
