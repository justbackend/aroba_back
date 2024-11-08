from django.db.models import Prefetch, F, Sum
from rest_framework import generics, views
from rest_framework.response import Response

import utils
from apps.clients import models as client_models
from apps.orders import models as order_models
from utils.choices import *
from . import serializers, models
from .models import MainCheckout
from ..orders.models import Order


class ReportOrdersListAPI(generics.ListAPIView):
    serializer_class = serializers.ReportSerializer

    def get_queryset(self):
        if not (payment_type := self.request.query_params.get('payment_type')):
            raise utils.APIException('Must provide payment type. Example: ?payment_type=cash')

        orders_qs = (
            order_models.Order.objects.filter(
                payment_type=payment_type,
                status__in=(OrderStatus.STARTED, OrderStatus.AT_FACTORY,
                            OrderStatus.LOADED, OrderStatus.LOCATION_ASSIGNED)
            )
            .annotate(loading_name=F('loading__name'), unloading_name=F('unloading__name'))
        )

        return (
            client_models.Client.objects
            .prefetch_related(Prefetch('orders', queryset=orders_qs))
            .filter(orders__isnull=False)
            .distinct()
        )


class CreateTransactionAPI(generics.ListCreateAPIView):
    filter_set_fields = ('type', 'status')
    queryset = models.Transaction.objects.all()

    serializer_classes = {
        'POST': serializers.CreateTransactionSerializer,
        'GET': serializers.TransactionListSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes[self.request.method]


class UpdateTransactionAPI(generics.UpdateAPIView):
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionStatusUpdateSerializer
    http_method_names = 'patch',


class BalanceView(views.APIView):
    def get(self, request):
        current_balance = MainCheckout.balance

        response = {'current_balance': current_balance}

        unpaid_orders = (
            Order.objects.filter(paid=False)
            .values('payment_type')
            .annotate(total=Sum('income', default=0))
        )

        for item in unpaid_orders:
            response[item['payment_type']] = item['total']

        return Response(response)


class CashSummaryListView(generics.ListAPIView):
    serializer_class = serializers.CashSummarySerializer
    filterset_fields = ('client', 'loading', 'unloading', )
    search_fields = ('code', 'car_number', 'driver_phone', )

    def get_queryset(self):
        return (
            order_models.Order.objects.filter(
                payment_type=OrderPaymentTypes.CASH,
                paid=True,
                status=OrderStatus.FINISHED,
            )
            .select_related('loading', 'unloading', 'client')
            .only('id', 'code', 'date', 'car_number', 'loading__name',
                  'unloading__name', 'client__name', 'total_amount', 'income')
        )
