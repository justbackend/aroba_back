from django.contrib import admin
from unfold import admin as u_admin

from . import models


@admin.register(models.Checkout)
class CheckoutAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'name', 'balance', 'created_at', 'updated_at')

    def has_add_permission(self, request): return False

    def has_delete_permission(self, request, obj=None): return False


@admin.register(models.Transaction)
class TransactionAdmin(u_admin.ModelAdmin):
    list_display = ('id', 'amount', 'type', 'status', 'created_at', 'updated_at')



