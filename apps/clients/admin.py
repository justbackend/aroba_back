from django.contrib import admin
from unfold import admin as u_admin
from . import models


@admin.register(models.Client)
class ClientAdmin(u_admin.ModelAdmin):
    class ClientRouteInline(admin.StackedInline):
        model = models.ClientRoute
        extra = 1

    list_display = ('id', 'name', 'phone', 'accounting_phone')
    list_display_links = ('id', 'name', 'phone')
    inlines = (ClientRouteInline,)


@admin.register(models.ClientRoute)
class ClientRouteAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'amount', 'loading', 'unloading', 'client')
