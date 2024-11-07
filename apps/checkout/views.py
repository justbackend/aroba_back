from django.db.models import Prefetch, F, Sum
from rest_framework import generics
from rest_framework.response import Response

import utils
from apps.clients import models as client_models
from apps.orders import models as order_models
from utils.choices import *
from . import serializers, models
from .models import MainCheckout
from .serializers import BalanceSerializer
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


class BalanceView(generics.GenericAPIView):
    serializer_class = BalanceSerializer

    def get(self, request):
        current_balance = MainCheckout.balance
        debt_cash_sum = Order.objects.filter(
            paid=False, payment_type=PaymentTypes.CASH
        ).aggregate(Sum('income'))['income__sum'] or 0.0

        debt_transfer_sum = Order.objects.filter(
            paid=False, payment_type=PaymentTypes.TRANSFER
        ).aggregate(Sum('income'))['income__sum'] or 0.0

        data = {
            'current_balance': current_balance,
            'debt_cash': debt_cash_sum,
            'debt_transfer': debt_transfer_sum,
        }
        return Response(data)
