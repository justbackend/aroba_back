from django.db.models import Prefetch, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

import utils
from apps.clients import models as client_models
from apps.orders import models as order_models
from utils.choices import *
from . import serializers


class ReportOrdersListAPI(generics.ListAPIView):
    serializer_class = serializers.ReportSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('orders__payment_type',)

    def get_queryset(self):
        if not (payment_type := self.request.query_params.get('orders__payment_type')):
            raise utils.APIException('Must provide payment type')

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
