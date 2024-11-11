from django.contrib import admin
from unfold import admin as u_admin
from . import models
from apps.orders.models import Order


@admin.register(models.AccountantInvoice)
class AccountantInvoiceAdmin(u_admin.ModelAdmin):

    class OrdersInline(u_admin.StackedInline):
        model = Order
        extra = 0

    list_display = ("id", "customer", "accounting_phone", 'inn', 'created_at')
    inlines = (OrdersInline,)
