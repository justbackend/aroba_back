from rest_framework import viewsets, status, views, generics
from . import models, serializers
from utils import choices


class NewOrdersListView(generics.ListAPIView):
    queryset = models.Order.objects.filter(status=choices.OrderStatus.NEW)
    serializer_class = serializers.NewOrdersListSerializer








