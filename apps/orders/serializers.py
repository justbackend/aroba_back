from rest_framework import serializers
from . import models


class NewOrdersListSerializer(serializers.ModelSerializer):
    loading = serializers.CharField(source='loading.name')
    unloading = serializers.CharField(source='unloading.name')

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
        )
