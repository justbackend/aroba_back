from utils import BaseModel, PhoneValidator
from utils.choices import *
from django.db import models


class AccountantInvoice(BaseModel):
    total_amount = models.DecimalField(max_digits=30, decimal_places=2, default=0, verbose_name="Amount")
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
    creator = models.ForeignKey(
        'users.User', on_delete=models.PROTECT, related_name='invoices', verbose_name='Creator', default=1
    )
    past_orders = models.ManyToManyField(
        'orders.Order', related_name='invoices', verbose_name='Past orders'
    )

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        db_table = 'accountant_invoices'
