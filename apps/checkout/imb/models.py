from django.db import models
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


