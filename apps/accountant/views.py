from django.db.models import F, Prefetch, Sum
from rest_framework import generics, status
from rest_framework.response import Response

import utils
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
            ).order_by('-id')
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
    orders_qs = (
        orders_models.Order.objects
        .filter(payment_type=OrderPaymentTypes.TRANSFER,
                status__in=(
                    OrderStatus.STARTED, OrderStatus.AT_FACTORY,
                    OrderStatus.LOADED, OrderStatus.LOCATION_ASSIGNED,
                ))
        .annotate(loading_name=F('loading__name'), unloading_name=F('unloading__name'))
    )

    invoices_qs = (
        models.AccountantInvoice.objects
        .prefetch_related(Prefetch('orders', queryset=orders_qs, to_attr='to_orders'))
        .filter(
            status__in=(InvoiceStatuses.PENDING, InvoiceStatuses.APPROVED),
            orders__isnull=False,
        ).order_by('-status').distinct()
    )

    def get_queryset(self):
        clients_qs = (
            client_models.Client.objects
            .prefetch_related(
                Prefetch('orders', queryset=self.orders_qs.filter(invoice__isnull=True), to_attr='to_orders'),
                Prefetch('invoices', queryset=self.invoices_qs, to_attr='to_invoices'),
            )
            .filter(orders__payment_type=OrderPaymentTypes.TRANSFER)
            .order_by('-id').distinct()
        )

        return clients_qs


class CreateInvoice(generics.GenericAPIView):
    serializer_class = serializers.CreateInvoiceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        orders_id = serializer.validated_data['orders']
        orders = orders_models.Order.objects.filter(id__in=orders_id, invoice__isnull=True)
        if not orders.exists():
            raise utils.APIException('Orders does not exists')

        client = orders[0].client

        total_amount = orders.aggregate(total=Sum('total_amount'))['total']
        invoice = self.create_invoice(client, total_amount)
        orders.update(invoice_id=invoice.id)
        invoice.past_orders.set(orders)
        return Response(dict(client_id=client.id), status=status.HTTP_201_CREATED)

    def create_invoice(self, client, total_amount) -> models.AccountantInvoice:
        return models.AccountantInvoice.objects.create(
            client=client,
            accounting_phone=client.accounting_phone,
            customer=client.customer,
            inn=client.inn,
            total_amount=total_amount,
            creator=self.request.user,
        )


class UpdateInvoice(generics.UpdateAPIView):
    serializer_class = serializers.UpdateInvoiceSerializer
    http_method_names = 'patch',

    def get_object(self):
        return utils.get_object(model=models.AccountantInvoice, id=self.kwargs['pk'])
