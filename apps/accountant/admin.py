from django.contrib import admin
from unfold import admin as u_admin
from . import models


@admin.register(models.AccountantInvoice)
class AccountantInvoiceAdmin(u_admin.ModelAdmin):
    list_display = ("id", "customer", "accounting_phone", 'inn', 'created_at')
