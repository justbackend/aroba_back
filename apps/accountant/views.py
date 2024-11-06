from rest_framework.response import Response
from rest_framework import generics
from apps.orders import models as orders_models
from utils.choices import *
from . import models, serializers


class AccountantOrderList(generics.ListAPIView):
    queryset = orders_models.Order.objects.filter(payment_type=OrderPaymentTypes.TRANSFER)
    serializer_class = serializers.AccountantOrdersSerializer



