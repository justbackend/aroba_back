from rest_framework import serializers
import utils
from utils import choices
from  .. import models


class AdditionalAmountSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    comment = serializers.CharField(required=False)
    file = serializers.FileField(required=False)

    def validate(self, attrs):
        if not (attrs.get('comment') or attrs.get('file')):
            raise utils.APIException('Must be a comment or file')
        return attrs

    def update(self, instance, validated_data):
        models.OrderPayment.objects.create(
            order=instance, type=choices.PaymentTypes.EXTRA, **validated_data
        )
        return validated_data
