from rest_framework import serializers
import utils
from utils.choices import *
from .. import models


class AdditionalAmountSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    comment = serializers.CharField(required=False)
    file = serializers.FileField(required=False)

    def validate(self, attrs):
        if not (attrs.get('comment') or attrs.get('file')):
            raise utils.APIException('Must be a comment or file')
        return attrs

    def update(self, instance, validated_data):
        user = self.context['request'].user
        models.OrderPayment.objects.create(
            order=instance, type=PaymentTypes.EXTRA, **validated_data
        )
        log_comment = (f"Summa qo'shib berildi: {validated_data['amount']}  \n"
                       f"Komentariya: {validated_data.get('comment')}")

        models.Order.create_log(instance, user, OrderLogActions.ADDITIONAL_AMOUNT, comment=log_comment)
        return validated_data
