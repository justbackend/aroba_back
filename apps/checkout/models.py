from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from utils import BaseModel


class Checkout(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name")
    balance = models.DecimalField(max_digits=30, decimal_places=2, default=0, verbose_name="Balance")

    class Meta:
        verbose_name = "Checkout"
        verbose_name_plural = "Checkout"
        db_table = "checkout"


@receiver(post_migrate)
def create_checkout(sender, **kwargs):
    """
    The aim of signal is create main  checkout
    """
    if not Checkout.objects.exists():
        Checkout.objects.create(name="Asosiy kassa", balance=0)
