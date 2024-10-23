from django.db import models


class OrderStatus(models.IntegerChoices):
    REJECTED = -1, "Rejected"
    DELETED = 0, "Deleted"
    NEW = 1, "New"
    FILLING = 2, "Filling"
    STARTED = 3, "Started"
    AT_FACTORY = 4, 'At Factory'
    LOADED = 5, "Dispatched"
    LOCATION_ASSIGNED = 6, 'Location assigned'
    FINISHED = 9, 'Finished'


class OrderPaymentType(models.TextChoices):
    TRANSFER = 'transfer', 'Transfer'
    CASH = 'cash', 'Cash'


class PaymentType(models.TextChoices):
    TRANSFER = 'transfer', 'Transfer'
    CASH = 'cash', 'Cash'
    EXTRA = 'extra', 'Extra'


API_ROUTE_CHOICES = (
    ('/api/v1/users/', 'Users'),
    ('/api/v1/common/', 'Common'),
)

API_DYNAMIC_CHOICES = (
    ('1', 'Yes'),
    ('0', 'No'),
)

