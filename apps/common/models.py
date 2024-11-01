from django.db import models
from django.db.models.signals import pre_migrate
from django.dispatch import receiver


from . import managers


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = managers.Manager()

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
    deleted = models.BooleanField(default=False, verbose_name="Deleted")

    objects = models.Manager()
    active_objects = managers.ActivePointManager()

    class Meta:
        db_table = 'points'

    def __str__(self):
        return self.name


# @receiver(pre_migrate)
# def pre_migrate_signal(sender, **kwargs):
#
#     from core.scheduler import start_scheduler
#     start_scheduler()
#
#     print('the tasks')
