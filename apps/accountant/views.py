from django.db.models import F, Prefetch
from rest_framework import generics

from apps.clients import models as client_models
from apps.orders import models as orders_models
from utils.choices import *
from utils.excel import ExcelListView
from . import serializers, models


class TransClientsViewList(generics.ListAPIView):
    serializer_class = serializers.TransClientSerializer

    def get_queryset(self):
        return (
            client_models.Client.objects
            .filter(routes__type=ClientRouteTypes.TRANSFER)
            .distinct()
        )


class TransClientsViewUpdate(generics.UpdateAPIView):
    serializer_class = serializers.TransClientSerializer
    queryset = client_models.Client.objects.all()
    http_method_names = 'patch',


class TransClientsViewExcel(ExcelListView, TransClientsViewList):
    fields = ('id', 'customer', 'accounting_phone', 'inn', 'requisite')

    def get_data(self):
        return self.get_queryset()


class FinishedOrders(generics.ListAPIView):
    serializer_class = serializers.FinishedOrdersSerializer

    def get_queryset(self):
        return (
            orders_models.Order.objects
            .select_related('loading', 'unloading', 'client')
            .filter(
                payment_type=OrderPaymentTypes.TRANSFER,
                status=OrderStatus.FINISHED,
            )
        )


class FinishedOrdersExcel(ExcelListView, FinishedOrders):
    filename = 'finished_orders'
    fields = (
        'client_name', 'date', 'loading_name',
        'unloading_name', 'car_number', 'total_amount'
    )
    default_widths = 30

    def get_data(self):
        return (
            self.get_queryset()
            .annotate(
                client_name=F('client__name'),
                loading_name=F('loading__name'),
                unloading_name=F('unloading__name'),
            ))


class InvoiceOrders(generics.ListAPIView):
    serializer_class = serializers.InvoiceOrdersSerializer

    invoices_qs = models.AccountantInvoice.objects.filter()

    orders_qs = (
        orders_models.Order.objects
        .filter(payment_type=OrderPaymentTypes.TRANSFER, invoice__isnull=True)
        .annotate(loading_name=F('loading__name'), unloading_name=F('unloading__name'))
    )

    def get_queryset(self):
        clients_qs = (
            client_models.Client.objects
            .prefetch_related(Prefetch('orders', queryset=self.orders_qs, to_attr='to_orders'))
            .filter(orders__payment_type=OrderPaymentTypes.TRANSFER)
            .order_by('-id').distinct()
        )

        return clients_qs
