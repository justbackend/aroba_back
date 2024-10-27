from django.contrib import admin
from . import models


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    class PointInline(admin.StackedInline):
        model = models.Point
        extra = 1

    list_display = ('id', 'name')
    inlines = (PointInline,)


@admin.register(models.Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'deleted')
