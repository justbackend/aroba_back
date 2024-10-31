from rest_framework import generics

from utils import *
from . import serializers


class CreateOrderView(generics.CreateAPIView):
    permission_classes = (IsActive,)
    serializer_class = serializers.CreateOrderSerializer
