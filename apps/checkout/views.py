from django.db.models import Prefetch, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import utils
from apps.clients import models as client_models
from apps.orders import models as order_models
from utils.choices import *
from . import serializers, models

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

