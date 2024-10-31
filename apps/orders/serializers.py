from rest_framework import serializers
from . import models
import utils


class NewOrdersListSerializer(serializers.ModelSerializer):
    loading = serializers.CharField(source='loading.name')
    unloading = serializers.CharField(source='unloading.name')
    client = serializers.CharField(source='client.name')
    dispatcher = utils.UserNameSerializer()

    class Meta:
        model = models.Order
        fields = (
            'id',
            'code',
            'date',
            'comment',
            'payment_type',
            'created_at',
            'loading',
            'unloading',
            'client',
        )
