import random
import string

from django.db import models

from apps.common.models import BaseModel
from utils import choices
import utils


class Order(BaseModel):
    code = models.CharField(max_length=20, unique=True, verbose_name="Code")
    date = models.DateField(auto_now_add=True, verbose_name="Date")
    paid = models.BooleanField(default=False, verbose_name="Is Paid")
    comment = models.TextField(verbose_name="Comment", null=True, blank=True)
    payment_type = models.CharField(max_length=15, choices=choices.OrderPaymentTypes.choices)
    income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Income", null=True, blank=True)
    status = models.IntegerField(choices=choices.OrderStatus.choices, default=choices.OrderStatus.NEW)
    car_number = models.CharField(
        max_length=20, verbose_name="Cart Number",
        null=True, blank=True,
        validators=[utils.VehicleNumberValidator()]
    )
    driver_phone = models.CharField(
        max_length=20, verbose_name="Driver Phone",
        null=True, blank=True,
        validators=[utils.PhoneValidator()]
    )
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Total Amount", null=True,
        blank=True
    )
    loading = models.ForeignKey(
        'common.Point', on_delete=models.PROTECT, related_name='orders_loading', verbose_name="Loading",
    )
    unloading = models.ForeignKey(
        'common.Point', on_delete=models.PROTECT, related_name='orders_unloading', verbose_name="Un Loading",
    )
    client = models.ForeignKey(
        'clients.Client', on_delete=models.PROTECT, related_name='orders', verbose_name="Client",
    )
    creator = models.ForeignKey(
        'users.User', on_delete=models.PROTECT, related_name='orders_creator', verbose_name="Creator",
    )
    dispatcher = models.ForeignKey(
        'users.User', on_delete=models.PROTECT,
        related_name='orders_dispatcher', verbose_name="Dispatcher",
        null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        db_table = 'orders'

    @classmethod
    def generate_code(cls):
        while True:
            numbers = ''.join(random.choices(string.digits, k=2))
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            code = f"{numbers}{letters}"
            if not cls.objects.filter(code=code).exists():
                return code

    @classmethod
    def generate_codes(cls, count) -> list[str]:

        result = []

        for i in range(count):
            code = cls.generate_code()
            if code not in result:
                result.append(cls.generate_code())
        return result


class OrderPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    type = models.CharField(max_length=15, choices=choices.PaymentTypes.choices, verbose_name="Type")
    comment = models.TextField(verbose_name="Comment", null=True, blank=True)
    file = models.FileField(verbose_name="File", null=True, blank=True, upload_to="payments/")
    order = models.ForeignKey(Order, verbose_name="Order", on_delete=models.PROTECT, related_name="payments", )

    class Meta:
        verbose_name = 'Order Payment'
        verbose_name_plural = 'Order Payments'
        db_table = 'order_payments'
        constraints = [
            models.UniqueConstraint(fields=['order', 'type'], name='unique_order_type')
        ]
