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


class OrderPaymentTypes(models.TextChoices):
    TRANSFER = 'transfer', 'Transfer'
    CASH = 'cash', 'Cash'


class PaymentTypes(models.TextChoices):
    TRANSFER = 'transfer', 'Transfer'
    CASH = 'cash', 'Cash'
    EXTRA = 'extra', 'Extra'


class APIMethods(models.TextChoices):
    POST = 'POST', 'POST'
    PUT = 'PUT', 'PUT'
    DELETE = 'DELETE', 'DELETE'
    PATCH = 'PATCH', 'PATCH'
    GET = 'GET', 'GET'


class APIRoutes(models.TextChoices):
    USERS = '/api/v1/users/', 'Users'
    COMMON = '/api/v1/common/', 'Common'
    CLIENTS = '/api/v1/clients/', 'Clients'
    ORDERS = '/api/v1/orders/', 'Orders'
    AUTH = '/api/v1/auth/', 'Auth'


class ClientRouteTypes(models.TextChoices):
    TRANSFER = 'transfer', 'Transfer'
    CASH = 'cash', 'Cash'
