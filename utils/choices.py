from django.db import models


class OrderStatus(models.IntegerChoices):
    REJECTED = -1, "Rejected"
    DELETED = 0, "Deleted"
    NEW = 1, "New"
    FILLING = 2, "Filling"
    STARTED = 3, "Started"
    AT_FACTORY = 4, 'At Factory'
    LOADED = 5, "Loaded"
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
    MANAGERS = '/api/v1/managers/', 'Managers'
    DISPATCHERS = '/api/v1/dispatchers/', 'Dispatchers'
    CHECKOUT = '/api/v1/checkout/', 'Checkout'


class ClientRouteTypes(models.TextChoices):
    TRANSFER = 'transfer', 'Transfer'
    CASH = 'cash', 'Cash'


class OrderLogActions(models.TextChoices):
    CREATE = 'create', 'Create'
    UPDATE = 'update', 'Update'
    DELETE = 'delete', 'Delete'
    AMOUNT = 'amount', 'Amount'
    ADDITIONAL_AMOUNT = 'additional_amount', 'Additional Amount'
    FILLED = 'filled', 'Filled'
    ROLLBACK = 'rollback', 'Rollback'


class TransactionTypes(models.TextChoices):
    INCOME = 'income', 'Income'
    EXPENSE = 'expense', 'Expense'


class TransactionStatuses(models.TextChoices):
    PENDING = 'pending', 'Pending'
    CANCELLED = 'cancelled', 'Cancelled'
    APPROVED = 'approved', 'Approved'


class InvoiceStatuses(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    CANCELLED = 'cancelled', 'Cancelled'
