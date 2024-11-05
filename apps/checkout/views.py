from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import views, generics
from . import models, serializers
from apps.orders import models as order_models
from apps.clients import models as client_models


class ReportOrdersListAPI(generics.ListAPIView):
    serializer_class = serializers.ReportSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('orders__payment_type',)

    def get_queryset(self):

        qs = client_models.Client.objects.filter(orders__isnull=False).distinct()
        return qs
