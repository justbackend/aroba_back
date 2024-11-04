from rest_framework import serializers
from .. import models
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
        orders = models.Order.objects.bulk_create(order_objs)
        self.create_logs(orders)
        return validated_data

    def create_logs(self, orders):
        user = self.validated_data['creator']
        logs = list(map(lambda order: models.OrderLog(order=order, user_id=user.id), orders))
        models.OrderLog.objects.bulk_create(logs)
        return logs

    def to_representation(self, instance):
        return dict(codes=self.codes)


class OrderClientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
