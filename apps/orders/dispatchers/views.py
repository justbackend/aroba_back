from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Func, Value, Q, TextField
from django.db.models.functions import Concat
from rest_framework import generics, views
from rest_framework.response import Response

from utils import *
from utils.choices import *
from . import serializers
from .. import models
from ..utils import SocketSendOrders


class NewOrdersListView(generics.ListAPIView):
    serializer_class = serializers.NewOrdersListSerializer
    filterset_fields = ('client',)
    pagination_class = None

    def get_queryset(self):
        return (
            models.Order.objects.filter(status__in=(OrderStatus.NEW, OrderStatus.FILLING))
            .select_related('client', 'loading', 'unloading', 'dispatcher')
            .only(
                'id', 'code', 'date', 'comment', 'payment_type', 'created_at', 'loading__name',
                'unloading__name', 'client__name', 'dispatcher__last_name', 'dispatcher__first_name',
            )
        )


class BookOrRollbackOrderView(views.APIView):

    def get(self, request, order_id, *args, **kwargs):
        order = get_object(models.Order, id=order_id, status__in=(OrderStatus.NEW, OrderStatus.FILLING))
        user = request.user

        if order.dispatcher and order.dispatcher != user:
            raise APIException('User is not allowed to book orders.')

        order.dispatcher = None if order.dispatcher else user
        order.status = OrderStatus.FILLING if order.status == OrderStatus.NEW else OrderStatus.NEW
        order.save()

        SocketSendOrders.ws_dispatcher_orders(order, action='u')
        return Response()


class FillingOrdersListView(generics.ListAPIView):
    serializer_class = serializers.FillingOrdersListSerializer

    def get_queryset(self):
        abs_uri = self.request.build_absolute_uri('/')
        user = self.request.user
        query = dict(status=OrderStatus.FILLING, dispatcher=user)

        if 1 in user.roles.all().values_list('id', flat=True):
            query.pop('dispatcher', None)

        return (
            models.Order.objects.filter(**query)
            .select_related('client', 'loading', 'unloading')
            .only(
                'id', 'code', 'date', 'comment', 'payment_type', 'created_at', 'loading__name',
                'unloading__name', 'client__name', 'total_amount', 'car_number', 'driver_phone',
            )
            .annotate(extra_amount=ArrayAgg(
                Func(
                    Value('amount'), 'payments__amount',
                    Value('comment'), 'payments__comment',
                    Value('file'),
                    Concat(Value(f'{abs_uri}media/'), 'payments__file'),
                    function='JSON_BUILD_OBJECT',
                    output_field=TextField()
                ), filter=Q(payments__type=PaymentTypes.EXTRA)))
            .order_by('-id')
        )


class FillingOrderView(generics.UpdateAPIView):
    http_method_names = 'patch',
    serializer_class = serializers.FillOrderSerializer

    def get_object(self):
        return get_object(models.Order, id=self.kwargs['order_id'], status=OrderStatus.FILLING)

    def perform_update(self, serializer):
        serializer.save()
        # SocketSendOrders.ws_filling_orders(order=serializer.instance, action='d')
        # SocketSendOrders.ws_status_orders(order=serializer.instance, action='c')
        SocketSendOrders.ws_status_orders(order=serializer.instance, action='d')
