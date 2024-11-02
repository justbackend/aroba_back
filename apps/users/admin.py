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
    class ActionsInline(admin.StackedInline):
        model = models.Action
        extra = 1

    list_display = ('id', 'name', )
    inlines = (ActionsInline,)


@admin.register(models.Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'codename', 'name',)


@admin.register(models.APIRoute)
class APIRouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'dynamic', 'method')
