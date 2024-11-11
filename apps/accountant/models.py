from django.db import models
from utils import BaseModel, PhoneValidator
from utils.choices import *


class AccountantInvoice(BaseModel):
    status = models.CharField(choices=InvoiceStatuses.choices, default=InvoiceStatuses.PENDING)
    customer = models.CharField('Customer', max_length=50)
    inn = models.CharField(max_length=15, verbose_name="Inner client")
    accounting_phone = models.CharField(
        max_length=20, verbose_name="Accounting phone number",
        validators=[PhoneValidator()]
    )

    client = models.ForeignKey(
        'clients.Client', on_delete=models.PROTECT, related_name='invoices', verbose_name='Client'
    )

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        db_table = 'accountant_invoices'
