from django.contrib import admin
from unfold import admin as u_admin
from . import models


@admin.register(models.Region)
class RegionAdmin(u_admin.ModelAdmin):
    class PointInline(u_admin.StackedInline):
        model = models.Point
        extra = 1

    list_display = ('id', 'name')
    inlines = (PointInline,)


@admin.register(models.Point)
class PointAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'deleted')
