from django.contrib import admin
from . import models


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username',)


@admin.register(models.Module)
class ContentTypeAdmin(admin.ModelAdmin):
    class PermissionsInline(admin.StackedInline):
        model = models.Permission
        extra = 1

    class ExtendedModuleInline(admin.StackedInline):
        model = models.ExtendedModule
        extra = 1

    list_display = ('id', 'app_label', 'model')
    inlines = (ExtendedModuleInline, PermissionsInline)


@admin.register(models.Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'codename', 'name',)
