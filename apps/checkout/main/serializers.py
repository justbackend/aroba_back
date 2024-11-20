from rest_framework import serializers

import utils
from utils.choices import TransactionStatuses
from apps.checkout import models
from apps.checkout.models import MainCheckout


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
    client_paid = serializers.BooleanField(read_only=True)
    status = serializers.IntegerField(read_only=True)
    invoice_status = serializers.CharField(read_only=True)


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
    created_at = serializers.DateTimeField(read_only=True, format='%d.%m.%Y')
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Transaction
        fields = (
            'id',
            'comment',
            'amount',
            'creator',
            'status',
            'created_at',
        )
        extra_kwargs = {
            'status': {'read_only': True},
        }

    def validate(self, data):
        if MainCheckout.balance < data['amount'] or data['amount'] == 0:
            raise utils.APIException("Asosiy balansda mablag' yetarli emas")
        return data

    def create(self, validated_data):
        trans = super().create(validated_data)
        return trans


class TransactionListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, format='%d.%m.%Y')

    class Meta:
        model = models.Transaction
        fields = (
            'id',
            'amount',
            'status',
            'type',
            'comment',
            'created_at',
        )


class TransactionStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ('status', 'rejected')
        extra_kwargs = {
            'status': {'required': True},
        }

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
        MainCheckout.add(instance.amount)

    @staticmethod
    def cancelled(instance):
        pass


class CashSummarySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(read_only=True)
    date = serializers.DateField(read_only=True)
    car_number = serializers.CharField(read_only=True)
    loading = serializers.CharField(read_only=True, source='loading.name')
    unloading = serializers.CharField(read_only=True, source='unloading.name')
    client = serializers.CharField(read_only=True, source='client.name')
    total_amount = serializers.IntegerField(read_only=True)
    payment_type = serializers.CharField(read_only=True)
    paid = serializers.BooleanField(read_only=True)
