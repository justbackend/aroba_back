from django.contrib import admin
from . import models


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username',)


@admin.register(models.ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    class PermissionsInline(admin.StackedInline):
        model = models.Permission
        extra = 1

    class ExtendedContentTypeInline(admin.StackedInline):
        model = models.ExtendedContentType
        extra = 1

    list_display = ('id', 'app_label', 'model')
    inlines = (ExtendedContentTypeInline, PermissionsInline)
