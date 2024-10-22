from django.contrib import admin
from . import models


@admin.register(models.API)
class APIAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'role')
