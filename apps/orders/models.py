from django.db import models
from apps.common.models import BaseModel
from utils import choices


class Order(BaseModel):
    loading = ...
    unloading = ...
    client = ...
    code = models.CharField(max_length=20, unique=True, verbose_name="Code")
    date = models.DateField(auto_now_add=True, verbose_name="Date")
    car_number = models.CharField(max_length=20, verbose_name="Cart Number", null=True, blank=True)
    driver_phone = models.CharField(max_length=20, verbose_name="Driver Phone", null=True, blank=True)
    paid = models.BooleanField(default=False, verbose_name="Is Paid")
    comment = models.TextField(verbose_name="Comment", null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount", null=True,
                                       blank=True)
    payment_type = ...
    creator = ...
    income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Income", null=True, blank=True)
    status = models.IntegerField(
        choices=[(status.value, status.name) for status in choices.OrderStatus],
        default=choices.OrderStatus.NEW.value
    )


class OrderPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount", null=True, blank=True)
    type = ...
    comment = models.TextField(verbose_name="Comment", null=True, blank=True)
    file = models.FileField(verbose_name="File", null=True, blank=True, upload_to="payments/")
    order = models.ForeignKey(Order, verbose_name="Order", on_delete=models.PROTECT, related_name="payments", )
