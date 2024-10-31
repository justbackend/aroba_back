from rest_framework import serializers
import utils
from utils.choices import *
from .. import models


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


class FillingOrdersListSerializer(serializers.ModelSerializer):
    loading = serializers.CharField(source='loading.name')
    unloading = serializers.CharField(source='unloading.name')
    client = serializers.CharField(source='client.name')
    extra_amount = serializers.SerializerMethodField()

    def get_extra_amount(self, obj):
        return obj.extra_amount[0] if obj.extra_amount else None

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
            'car_number',
            'driver_phone',
            'total_amount',
            'extra_amount',
        )


class FillOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = (
            'id',
            'client',
            'loading',
            'unloading',
            'driver_phone',
            'car_number',
            'total_amount',
        )

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)
        log_comment = (
            f"Buyurtam qo'ldirldi\n"
            f"Clinet: {validated_data.get('client')}"
            f"Loading: {validated_data.get('loading')}"
            f"Unloading: {validated_data.get('unloading')}"
            f"Driver Phone: {validated_data.get('driver_phone')}"
            f"Car Number: {validated_data.get('car_number')}"
            f"Total Amount: {validated_data.get('total_amount')}"
        )
        models.Order.create_log(
            order=obj, comment=log_comment, action=OrderLogActions.FILLED, user=self.context['request'].user
        )
        return obj
