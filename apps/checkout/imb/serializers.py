from rest_framework import serializers

from .. import models


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
        )
        extra_kwargs = {
            'type': {'read_only': True},
        }
