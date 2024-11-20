from rest_framework import serializers

import utils
from apps.clients import models as client_models
from apps.common import models as common_models
from .. import models
from ..utils import SocketSendOrders


class CreateOrderSerializer(serializers.Serializer):
    loading = serializers.PrimaryKeyRelatedField(queryset=common_models.Point.objects.all())
    unloading = serializers.PrimaryKeyRelatedField(queryset=common_models.Point.objects.all())
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    client = serializers.PrimaryKeyRelatedField(queryset=client_models.Client.objects.all())
    car_count = serializers.IntegerField(default=1, max_value=30)
    comment = serializers.CharField(required=False)

    def validate(self, attrs):
        checking = client_models.ClientRoute.objects.filter(
            loading=attrs['loading'],
            unloading=attrs['unloading'],
            client=attrs['client'],
        ).exists()
        if not checking:
            raise utils.APIException("The client route does not exist")
        return attrs

    def create(self, validated_data):
        car_count = validated_data.pop('car_count')
        validated_data['payment_type'] = validated_data.get('client').type
        self.codes: set = models.Order.generate_codes(car_count)
        order_objs = list(map(lambda code: models.Order(code=code, **validated_data), self.codes))
        orders = models.Order.objects.bulk_create(order_objs)
        self.create_logs(orders)
        self.send_ws_dispatcher_orders(orders)
        return validated_data

    def create_logs(self, orders):
        user = self.validated_data['creator']
        comment = "Buyurtma Yaratildi"
        logs = list(map(lambda order: models.OrderLog(order=order, user_id=user.id, comment=comment), orders))
        models.OrderLog.objects.bulk_create(logs)
        return logs

    def send_ws_dispatcher_orders(self, orders):
        for order in orders:
            SocketSendOrders.ws_dispatcher_orders(order=order, action='c')

    def to_representation(self, instance):
        return dict(codes=self.codes)
