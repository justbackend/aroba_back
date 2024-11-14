from rest_framework import serializers
from .. import models, utils
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
        checking = client_models.ClientRoute.objects.filter(
            loading=attrs['loading'],
            unloading=attrs['unloading'],
            client=attrs['client'],
            type=attrs['payment_type'],
        ).exists()
        if not checking:
            raise utils.APIException("The client route does not exist")
        return attrs

    def create(self, validated_data):
        car_count = validated_data.pop('car_count')
        self.codes: set = models.Order.generate_codes(car_count)
        order_objs = list(map(lambda code: models.Order(code=code, **validated_data), self.codes))
        orders = models.Order.objects.bulk_create(order_objs)
        self.create_logs(orders)
        return validated_data

    def create_logs(self, orders):
        user = self.validated_data['creator']
        comment = "Buyurtma Yaratildi"
        logs = list(map(lambda order: models.OrderLog(order=order, user_id=user.id, comment=comment), orders))
        models.OrderLog.objects.bulk_create(logs)
        return logs

    def send_ws_dispatcher_orders(self, orders):

        for order in orders:
            utils.SocketSendOrders.ws_dispatcher_orders(order=order, action='c')

    def to_representation(self, instance):
        return dict(codes=self.codes)
