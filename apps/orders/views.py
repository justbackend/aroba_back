from rest_framework import viewsets, status, views, generics
from . import models, serializers
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


class CreateOrderView(generics.CreateAPIView):
    permission_classes = (IsActive,)
    serializer_class = serializers.CreateOrderSerializer
