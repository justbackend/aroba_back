from django.db import models

import utils
from apps.clients.models import ClientRoute
from utils import choices
from utils.base import BaseModel


class Order(BaseModel):
    code = models.CharField(max_length=20, unique=True, verbose_name="Code")
    date = models.DateField(auto_now_add=True, verbose_name="Date")
    paid = models.BooleanField(default=False, verbose_name="Is Paid")
    comment = models.TextField(verbose_name="Comment", null=True, blank=True)
    rejected_comment = models.TextField(verbose_name="Comment", null=True, blank=True)
    payment_type = models.CharField(max_length=15, choices=choices.OrderPaymentTypes.choices)
    income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Income", null=True, blank=True)
    status = models.IntegerField(choices=choices.OrderStatus.choices, default=choices.OrderStatus.NEW)
    car_number = models.CharField(
        max_length=20, verbose_name="Car Number",
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

    def __str__(self):
        return self.code

    @classmethod
    def generate_code(cls, serial_id: int) -> str:
        return str(serial_id)[:2] + ''.join(chr(int(i) + 65) for i in str(serial_id)[2:])

    # @classmethod
    # def generate_code(cls):
    #     while True:
    #         numbers = ''.join(random.choices(string.digits, k=2))
    #         letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    #         code = f"{numbers}{letters}"
    #         if not cls.objects.filter(code=code).exists():
    #             return code

    # @classmethod
    # def generate_codes(cls, count) -> list[str]:
    #
    #     result = []
    #     for i in range(count):
    #         code = cls.generate_code()
    #         if code not in result:
    #             result.append(cls.generate_code())
    #
    #     return result

    @classmethod
    def create_log_cls(cls, order, user, action, comment=None):
        return OrderLog.objects.create(order=order, user=user, comment=comment, action=action)

    def create_log(self, user, action, comment=None):
        return OrderLog.objects.create(order=self, user=user, comment=comment, action=action)

    @classmethod
    def cls_create_payment(cls, order, user, amount, _type):
        return OrderPayment.objects.create(order=order, user=user, amount=amount, type=_type)

    def create_payment(self, amount, _type, **kwargs):
        return OrderPayment.objects.create(order=self, amount=amount, type=_type, **kwargs)

    def set_income(self):

        route = ClientRoute.objects.filter(
            loading=self.loading,
            unloading=self.unloading,
            client=self.client,
            type=self.payment_type,
        ).first()

        if route and route.amount:
            setattr(self, 'income', route.amount)
        return self.income

    def clear(self, fields=()):
        """
        The method clear instance according to fields
        """
        for field in fields:
            if hasattr(self, field):
                setattr(self, field, None)


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


class OrderLog(BaseModel):
    order = models.ForeignKey(Order, verbose_name="Order", on_delete=models.CASCADE, related_name="logs")
    user = models.ForeignKey('users.User', verbose_name="User", on_delete=models.CASCADE)
    comment = models.CharField(verbose_name="Text", null=True, blank=True, max_length=255)
    action = models.CharField(
        max_length=20, verbose_name="Action",
        choices=choices.OrderLogActions.choices,
        default=choices.OrderLogActions.CREATE
    )

    class Meta:
        verbose_name = 'Order Log'
        verbose_name_plural = 'Order Logs'
        db_table = 'order_logs'
