from rest_framework.response import Response
from rest_framework import status, views, generics, viewsets
from . import serializers
from .. import models
from utils import *


class AdditionalAmountView(generics.UpdateAPIView):
    serializer_class = serializers.AdditionalAmountSerializer

    def get_object(self):
        return get_object(models.Order, id=self.kwargs['pk'])
