from django.db import models

from utils import CheckoutManager
from utils.choices import IMBTransactionTypes, IMBTransactionStatuses
from . import managers


class IMBCheckout(models.Model):
    balance = models.DecimalField(max_digits=14, decimal_places=2)
    objects = managers.IMBDatabaseManager()

    class Meta:
        verbose_name = 'IMB Checkout'
        verbose_name_plural = 'IMB Checkout'
        managed = False
        db_table = 'KassaApp_kassa'

    def save(self, *args, **kwargs):
        """
        Override save method to always use the 'imb' database.
        """
        kwargs['using'] = 'imb'
        super().save(*args, **kwargs)

    @classmethod
    def db(cls):
        return cls.objects.using('imb')

    @staticmethod
    def create_transaction(amount, _type, comment=None, status=IMBTransactionStatuses.APPROVED):
        IMBTransaction.objects.create(
            status=status,
            amount=amount,
            type=_type,
            comment=comment,
        )


class IMBTransaction(models.Model):
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

    objects = managers.IMBDatabaseManager()

    class Meta:
        verbose_name = 'IMB Transaction'
        verbose_name_plural = 'IMB Transactions'
        managed = False
        db_table = 'KassaApp_transactions'

    def save(self, *args, **kwargs):
        """
        Override save method to always use the 'imb' database.
        """
        kwargs['using'] = 'imb'
        super().save(*args, **kwargs)

    @classmethod
    def db(cls):
        return cls.objects.using('imb')


CheckoutIMB = CheckoutManager(model=IMBCheckout, balance_field='balance')
