from rest_framework import serializers
from . import models
import utils


class CreateOrderSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Order
        fields = (
            'id',
            'code',
            'loading',
            'unloading',
            'creator',
            'client',
            'payment_type',
        )

        extra_kwargs = {
            'code': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['code'] = models.Order.generate_code()
        return super().create(validated_data)


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
            'dispatcher',
        )
