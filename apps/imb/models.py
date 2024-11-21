from django.db import models

from utils import CheckoutManager
from utils.choices import IMBTransactionTypes, IMBTransactionStatuses
from . import managers


class Model(models.Model):
    objects = managers.IMBDatabaseManager()

    @classmethod
    def db(cls):
        return cls.objects.using('imb')

    def save(self, *args, **kwargs):
        """
        Override save method to always use the 'imb' database.
        """
        kwargs['using'] = 'imb'
        super().save(*args, **kwargs)


class IMBCheckout(Model):
    balance = models.DecimalField(max_digits=14, decimal_places=2)
    objects = managers.IMBDatabaseManager()

    class Meta:
        verbose_name = 'IMB Checkout'
        verbose_name_plural = 'IMB Checkout'
        managed = False
        db_table = 'KassaApp_kassa'

    @classmethod
    def db(cls):
        return cls.objects.using('imb')

    @staticmethod
    def create_transaction(amount, _type, comment=None, status=IMBTransactionStatuses.APPROVED):
        Transactions.objects.create(
            status=status,
            amount=amount,
            type=_type,
            comment=comment,
        )


class Transactions(Model):
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    comment = models.CharField(max_length=250)
    type = models.IntegerField(choices=IMBTransactionTypes.choices, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    check_url = models.URLField(max_length=50, null=True, blank=True, verbose_name="Check")
    status = models.CharField(
        max_length=50, verbose_name="Status",
        choices=IMBTransactionStatuses.choices,
        default=IMBTransactionStatuses.APPROVED
    )


CheckoutIMB = CheckoutManager(model=IMBCheckout, balance_field='balance')
