from django.contrib import admin
from . import models


@admin.register(models.AccountantInvoice)
class AccountantInvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "accounting_phone", 'inn', 'created_at')
