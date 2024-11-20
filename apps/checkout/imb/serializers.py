from rest_framework import serializers

from utils.choices import TransactionStatuses
from .. import models
from ..models import MainCheckout


class IMBTransactionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = models.Transaction
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
        model = models.Transaction
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
            }[status](instance)

        obj = super().update(instance, validated_data)
        return obj

    @staticmethod
    def approved(instance):
        MainCheckout.add(-instance.amount)

    @staticmethod
    def cancelled(instance):
        pass
