from django.contrib import admin
from . import models
from django.contrib.auth.models import Permission, ContentType
# from django.contrib.auth.decorators import permission_required
# from django.utils.decorators import method_decorator


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


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'codename', 'name',)


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    class PermissionInline(admin.StackedInline):
        model = Permission
        extra = 1

    list_display = ('id', 'app_label', 'model',)
    inlines = (PermissionInline,)
