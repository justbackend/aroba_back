from rest_framework import generics

import utils
from utils.permissions import *
from . import serializers
from apps.clients import models as clients_models


class CreateOrderView(generics.CreateAPIView):
    permission_classes = (IsActive,)
    serializer_class = serializers.CreateOrderSerializer


class ClientsListView(generics.ListAPIView):
    serializer_class = utils.create_serializer({'id': int, 'name': str})
    queryset = clients_models.Client.active_objects.all()
    pagination_class = None
