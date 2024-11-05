from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from utils import BaseModel
from utils.choices import TransactionTypes, TransactionStatuses


class Checkout(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name")
    balance = models.DecimalField(max_digits=30, decimal_places=2, default=0, verbose_name="Balance")

    class Meta:
        verbose_name = "Checkout"
        verbose_name_plural = "Checkout"
        db_table = "checkout"

    def __str__(self):
        return f"{self.name} ({self.balance})"


class Transaction(BaseModel):
    amount = models.DecimalField(max_digits=30, decimal_places=2, verbose_name="Amount")
    comment = models.CharField(max_length=255, verbose_name="Description", blank=True, null=True)
    type = models.CharField(
        max_length=20, verbose_name="Type",
        choices=TransactionTypes.choices,
    )
    status = models.CharField(
        max_length=20, verbose_name="Status",
        choices=TransactionStatuses.choices, default=TransactionStatuses.PENDING
    )
    creator = models.ForeignKey(
        'users.User', verbose_name="Creator",
        on_delete=models.PROTECT, related_name="transactions_creator"
    )
    checker = models.ForeignKey(
        'users.User', verbose_name="Checker",
        on_delete=models.PROTECT,  related_name="transactions_checker",
        null=True, blank=True
    )

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        db_table = "transactions"


def CHECKOUT() -> Checkout:
    return Checkout.objects.first()


@receiver(post_migrate)
def create_checkout(sender, **kwargs):
    """
    The aim of signal is create main  checkout
    """
    if not Checkout.objects.exists():
        Checkout.objects.create(name="Asosiy kassa", balance=0)
