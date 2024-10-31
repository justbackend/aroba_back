from rest_framework import generics
from django.db.models import Q
from utils import *
from utils.choices import PaymentTypes
from . import serializers
from .. import models


class AdditionalAmountView(generics.UpdateAPIView):
    serializer_class = serializers.AdditionalAmountSerializer
    http_method_names = 'patch',

    def get_object(self):
        return get_object(
            models.Order,
            ~Q(payments__type=PaymentTypes.EXTRA),
            id=self.kwargs['order_id'],
        )
