from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Sum, Func, Value, Q, JSONField, TextField, DecimalField, FileField, CharField
from django.db.models.functions import Cast, Concat
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, views
from rest_framework.response import Response

from .. import models
from . import serializers
from utils import choices
from utils import *


class NewOrdersListView(generics.ListAPIView):
    serializer_class = serializers.NewOrdersListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('client',)
    pagination_class = None

    def get_queryset(self):
        return (
            models.Order.objects.filter(status=choices.OrderStatus.NEW)
            .select_related('client', 'loading', 'unloading', 'dispatcher')
            .only(
                'id', 'code', 'date', 'comment', 'payment_type', 'created_at', 'loading__name',
                'unloading__name', 'client__name', 'dispatcher__last_name', 'dispatcher__first_name',
            )
        )


class BookOrRollbackOrderView(views.APIView):

    def get(self, request, order_id, *args, **kwargs):
        order = get_object(models.Order, id=order_id, status=choices.OrderStatus.NEW)
        user = request.user

        if order.dispatcher and order.dispatcher != user:
            raise APIException('User is not allowed to book orders.')

        order.dispatcher = None if order.dispatcher else user
        order.status = choices.OrderStatus.FILLING
        order.save()
        return Response()


class FillingOrdersListView(generics.ListAPIView):
    serializer_class = serializers.FillingOrdersListSerializer

    def get_queryset(self):
        return (
            models.Order.objects.filter(status=choices.OrderStatus.FILLING)
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
                    Concat(Value('http://localhost:8000/media/'), 'payments__file'),
                    function='JSON_BUILD_OBJECT',
                    output_field=TextField()
                ), filter=Q(payments__type=choices.PaymentTypes.EXTRA)))
        )
