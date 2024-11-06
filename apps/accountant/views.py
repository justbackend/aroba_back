from django.db.models import F
from rest_framework import generics

from apps.orders import models as orders_models
from utils.choices import *
from . import serializers
from utils.excel import ExcelListView


class AccountantOrderList(generics.ListAPIView):
    serializer_class = serializers.AccountantOrdersSerializer

    def get_queryset(self):
        return (
            orders_models.Order.objects
            .select_related('loading', 'unloading', 'client')
            .filter(
                payment_type=OrderPaymentTypes.TRANSFER,
                status__in=(OrderStatus.STARTED, OrderStatus.LOADED,
                            OrderStatus.AT_FACTORY, OrderStatus.LOCATION_ASSIGNED)
            )
        )


class AccountantOrdersExcel(ExcelListView, AccountantOrderList):
    filename = 'accountant_orders'
    fields = (
        'id', 'code', 'client_name', 'client_phone',
        'client_accounting_phone', 'loading_name', 'unloading_name', 'total_amount'
    )
    default_widths = 30

    def get_data(self):
        return (
            self.get_queryset()
            .annotate(
                client_name=F('client__name'),
                client_phone=F('client__phone'),
                client_accounting_phone=F('client__accounting_phone'),
                loading_name=F('unloading__name'),
                unloading_name=F('unloading__name'),
            )
        )
