from rest_framework import serializers

from utils.choices import TransactionStatuses
from . import models
from .models import MainCheckout


class ReportOrdersSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(read_only=True)
    date = serializers.DateField(read_only=True)
    loading_name = serializers.CharField(read_only=True)
    unloading_name = serializers.CharField(read_only=True)
    car_number = serializers.CharField(read_only=True)
    income = serializers.IntegerField(read_only=True)
    total_amount = serializers.IntegerField(read_only=True)
    paid = serializers.BooleanField(read_only=True)


class ReportSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    amounts = serializers.SerializerMethodField()
    orders = ReportOrdersSerializer(many=True)

    def get_amounts(self, obj):
        result = dict(sum_income=0, sum_total_amount=0)
        for order in obj.orders.all():
            result["sum_income"] += order.income or 0
            result["sum_total_amount"] += order.total_amount or 0
        return result


class CreateTransactionSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Transaction
        fields = (
            'id',
            'comment',
            'type',
            'amount',
            'creator',
            'status',
        )
        extra_kwargs = {
            'status': {'read_only': True},
        }


class TransactionStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ['status']

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)
        if obj.status == TransactionStatuses.APPROVED:
            amount = {
                'income': obj.amount,
                'expense': -obj.amount,
            }[obj.type]
            MainCheckout.add_balance(amount)

        return obj


class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = (
            'id',
            'amount',
            'status',
            'type',
            'comment',
        )


class BalanceSerializer(serializers.Serializer):
    current_balance = serializers.FloatField()
    debt_cash = serializers.FloatField()
    debt_transfer = serializers.FloatField()
