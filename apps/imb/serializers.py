from rest_framework import serializers

from utils.choices import TransactionStatuses, IMBTransactionTypes
from apps.checkout import models as checkout_models
from apps.checkout.models import MainCheckout
from .models import CheckoutIMB, IMBCheckout


class IMBTransactionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = checkout_models.Transaction
        fields = (
            'id',
            'amount',
            'receiver',
            'type',
            'comment',
            'rejected',
            'created_at',
            'status',
        )
        extra_kwargs = {
            'type': {'read_only': True},
        }


class IMBUpdateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = checkout_models.Transaction
        fields = (
            'id',
            'status',
            'rejected'
        )

    def update(self, instance, validated_data):
        status = validated_data['status']

        if status != TransactionStatuses.PENDING:
            {
                TransactionStatuses.CANCELLED: self.cancelled,
                TransactionStatuses.APPROVED: self.approved,
                TransactionStatuses.PENDING: self.pending,
            }[status](instance)

        obj = super().update(instance, validated_data)
        return obj

    @staticmethod
    def approved(instance):
        MainCheckout - instance.amount # noqa
        CheckoutIMB + instance.amount # noqa

        IMBCheckout.create_transaction(
            amount=instance.amount,
            _type=IMBTransactionTypes.AGENT_INCOME,
            comment=f"Arobadan kirim"
        )

    @staticmethod
    def cancelled(instance):
        pass

    @staticmethod
    def pending(instance):
        pass
