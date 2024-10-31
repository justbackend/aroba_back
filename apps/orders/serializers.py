from rest_framework import serializers
from . import models
import utils
from apps.common import models as common_models
from apps.clients import models as client_models
from utils import choices


class CreateOrderSerializer(serializers.Serializer):
    loading = serializers.PrimaryKeyRelatedField(queryset=common_models.Point.objects.all())
    unloading = serializers.PrimaryKeyRelatedField(queryset=common_models.Point.objects.all())
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    client = serializers.PrimaryKeyRelatedField(queryset=client_models.Client.objects.all())
    car_count = serializers.IntegerField(default=1)
    comment = serializers.CharField(required=False)
    payment_type = serializers.ChoiceField(choices=choices.OrderPaymentTypes.choices)

    def validate(self, attrs):

        if attrs['loading'] == attrs['unloading']:
            raise utils.APIException('The Point must not be same')
        return attrs

    def create(self, validated_data):
        car_count = validated_data.pop('car_count')
        self.codes: list = models.Order.generate_codes(car_count)

        order_objs = list(map(lambda code: models.Order(code=code, **validated_data), self.codes))
        models.Order.objects.bulk_create(order_objs)
        return validated_data

    def to_representation(self, instance):
        return self.codes


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
