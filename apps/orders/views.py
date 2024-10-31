from rest_framework import viewsets, status, views, generics
from . import models, serializers
from utils import choices


class NewOrdersListView(generics.ListAPIView):
    serializer_class = serializers.NewOrdersListSerializer
    pagination_class = None

    def get_queryset(self):
        return (
            models.Order.objects.filter(status=choices.OrderStatus.NEW)
            .select_related('client', 'loading', 'unloading', 'dispatcher')
            # .only(
            #     'id', 'code', 'date', 'comment', 'payment_type', 'created_at', 'loading__name',
            #     'unloading__name', 'client__name',
            # )
        )


class CreateOrderView(generics.CreateAPIView):
    serializer_class = serializers.CreateOrderSerializer
