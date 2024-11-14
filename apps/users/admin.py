from django.contrib import admin
from unfold import admin as u_admin
from . import models


@admin.register(models.Role)
class RoleAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.User)
class UserAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'username',)
    readonly_fields = ('actions',)


@admin.register(models.Action)
class ActionAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'module', 'name',)


@admin.register(models.Module)
class ContentTypeAdmin(u_admin.ModelAdmin):
    class ActionsInline(u_admin.StackedInline):
        model = models.Action
        extra = 1

    list_display = ('id', 'name',)
    inlines = (ActionsInline,)


@admin.register(models.Permission)
class PermissionAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'codename', 'name',)


@admin.register(models.APIRoute)
class APIRouteAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'name', 'dynamic', 'method')
