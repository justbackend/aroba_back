from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import generics, views
from django.db.models import Q
from rest_framework.filters import SearchFilter

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
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_fields = ('client', 'status', 'payment_type')
    search_fields = ('car_number', 'code', 'driver_phone')

    def get_queryset(self):
        return (
            models.Order.objects.filter(
                status__in=(OrderStatus.STARTED, OrderStatus.AT_FACTORY,
                            OrderStatus.LOADED, OrderStatus.LOCATION_ASSIGNED)
            ).select_related('loading', 'client', 'unloading')
        )


class RollbackOrderView(views.APIView):

    def get(self, request, order_id, *args, **kwargs):
        order = get_object(models.Order, ~Q(status=OrderStatus.NEW), id=order_id)
        order.clear(
            fields=('car_number', 'income', 'driver_phone', 'total_amount', 'dispatcher')
        )
        order.status = OrderStatus.NEW
        order.paid = False
        order.save()

        return Response({'msg': "Success"})


class UpdateOrderStatusView(generics.UpdateAPIView):
    serializer_class = serializers.UpdateOrderStatusSerializer
    http_method_names = 'patch',

    def get_object(self):
        return get_object(models.Order, id=self.kwargs['pk'])
