from django.db import models

from utils import CheckoutManager, BaseModel
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


class Contact(BaseModel):
    full_name = models.CharField(max_length=100, verbose_name='Full name')
    truck_id = models.CharField(max_length=30, verbose_name='Truck ID', null=True, blank=True)
    phone = models.CharField(max_length=9, verbose_name='Phone number', unique=True)
    car_type = models.CharField(max_length=30, null=True, verbose_name='Car Type')
    car_model = models.CharField(max_length=30, null=True, verbose_name='Car Model')
    trailer_type = models.CharField(max_length=30, null=True, verbose_name='Trailer Type')
    is_blocked = models.BooleanField(verbose_name='Is Blocked', default=False)
    is_contacted = models.BooleanField(verbose_name='Is Contacted', default=True)
    trailer_front = models.ImageField(
        null=True, blank=True,
        upload_to='contact_images/',
        verbose_name='Trailer front',
        # storage=PublicStorage
    )
    trailer_back = models.ImageField(
        null=True, blank=True,
        upload_to='contact_images/',
        verbose_name='Trailer back',
        # storage=PublicStorage
    )
    license_front = models.ImageField(
        null=True, blank=True,
        upload_to='contact_images/',
        verbose_name='License front',
        # storage=PublicStorage
    )
    license_back = models.ImageField(
        null=True, blank=True,
        upload_to='contact_images/',
        verbose_name='License back',
        # storage=PublicStorage
    )
    track_front = models.ImageField(
        null=True, blank=True,
        upload_to='contact_images/',
        verbose_name='Track front',
        # storage=PublicStorage
    )
    track_back = models.ImageField(
        null=True, blank=True,
        upload_to='contact_images/',
        verbose_name='Track back',
        # storage=PublicStorage
    )

    objects = managers.IMBDatabaseManager()

    class Meta:
        db_table = 'contacts'
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        managed = False

    @classmethod
    def db(cls):
        return cls.objects.using('imb')

    def __str__(self):
        return f'{self.full_name} - {self.truck_id}'

    def save(self, *args, **kwargs):
        self.full_name = str(self.full_name).upper()
        self.truck_id = str(self.truck_id).upper()
        self.car_type = str(self.car_type).upper()
        kwargs['using'] = 'imb'
        super().save(*args, **kwargs)


CheckoutIMB = CheckoutManager(model=IMBCheckout, balance_field='balance')
