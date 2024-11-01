from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.db.models import Q
from utils import *
from utils.choices import *
from . import serializers
from .. import models


class AdditionalAmountView(generics.UpdateAPIView):
    serializer_class = serializers.AdditionalAmountSerializer
    http_method_names = 'patch',

    def get_object(self):
        return get_object(
            models.Order,
            ~Q(payments__type=PaymentTypes.EXTRA),
            id=self.kwargs['order_id'],
        )


class StatusOrdersListView(generics.ListAPIView):
    serializer_class = serializers.StatusOrdersListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('client', 'status',)

    def get_queryset(self):
        return (
            models.Order.objects.filter(
                status__in=(OrderStatus.STARTED, OrderStatus.AT_FACTORY,
                            OrderStatus.LOADED, OrderStatus.LOCATION_ASSIGNED)
            ).select_related('loading', 'client', 'unloading')
            .only('id', 'code', 'car_number', 'driver_phone',
                  'date', 'loading__name', 'unloading__name', 'client__name',)
        )
