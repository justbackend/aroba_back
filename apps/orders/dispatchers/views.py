from rest_framework import generics, views
from rest_framework.response import Response

from .. import models
from . import serializers
from utils import choices
from utils import *


class NewOrdersListView(generics.ListAPIView):
    serializer_class = serializers.NewOrdersListSerializer
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
        order.dispatcher = None if order.dispatcher == user else user
        order.save()
        return Response()


