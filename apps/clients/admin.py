from django.contrib import admin
from . import models


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    class ClientRouteInline(admin.StackedInline):
        model = models.ClientRoute
        extra = 1

    list_display = ('id', 'name', 'phone', 'accounting_phone')
    inlines = (ClientRouteInline,)


@admin.register(models.ClientRoute)
class ClientRouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'loading', 'unloading', 'client')
