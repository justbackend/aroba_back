from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from . import models
from unfold.admin import ModelAdmin
from unfold import admin as u_admin

# admin.site.unregister(models.User)
# admin.site.unregister(Group)


# @admin.register(models.User)
# class UserAdmin(BaseUserAdmin, ModelAdmin):
#     list_display = ("username", "first_name", "last_name", "is_staff")
#     fieldsets = (
#         (None, {"fields": ("username", "password")}),
#         (_("Personal info"), {"fields": ("first_name", "last_name")}),
#         (
#             _("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                 ),
#             },
#         ),
#         (_("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )
#
#
# @admin.register(Group)
# class GroupAdmin(BaseGroupAdmin, ModelAdmin):
#     pass


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

    list_display = ('id', 'name', 'section')
    inlines = (ActionsInline,)


@admin.register(models.Permission)
class PermissionAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'codename', 'name',)


@admin.register(models.APIRoute)
class APIRouteAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'name', 'dynamic', 'method')


@admin.register(models.Section)
class SectionAdmin(u_admin.ModelAdmin):
    class ModuleInline(u_admin.StackedInline):
        model = models.Module
        extra = 1

    list_display = ('id', 'name')
    inlines = (ModuleInline,)
