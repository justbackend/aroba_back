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
    dispatcher = utils.UserNameSerializer()
    loading = utils.PointNameSerializer()
    unloading = utils.PointNameSerializer()
    client = utils.ClientNameSerializer()
    extra_amount = serializers.SerializerMethodField()

    def get_extra_amount(self, obj):
        return obj.extra_amount[0] if hasattr(obj, 'extra_amount') and obj.extra_amount else None

    class Meta:
        model = models.Order
        fields = (
            'id',
            'code',
            'date',
            'comment',
            'payment_type',
            'created_at',
            'car_number',
            'driver_phone',
            'total_amount',
            'extra_amount',
            'status',
            'dispatcher',
            'loading',
            'unloading',
            'client',
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
        for key, value in validated_data.items():
            if value:
                setattr(instance, key, value)

        if not instance.set_income():
            raise utils.APIException("The Client has not such a route or route has not amount")

        instance.status = OrderStatus.STARTED
        instance.save()

        instance.create_payment(amount=instance.total_amount, _type=instance.payment_type)
        log_comment = (
            f"Buyurtma qoldirldi:  \n"
            f"Client: {validated_data.get('client')}  \n\n"
            f"Loading: {validated_data.get('loading')}  \n\n"
            f"Unloading: {validated_data.get('unloading')}  \n\n"
            f"Driver Phone: {validated_data.get('driver_phone')}  \n\n"
            f"Car Number: {validated_data.get('car_number')}  \n\n"
            f"Total Amount: {validated_data.get('total_amount')}  \n\n"
        )
        instance.create_log(
            comment=log_comment, action=OrderLogActions.FILLED, user=self.context['request'].user
        )
        return instance


class FillingContactsListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    phone = serializers.CharField()
    truck_id = serializers.CharField()


