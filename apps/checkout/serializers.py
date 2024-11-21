from rest_framework import serializers

import utils
from apps.imb.models import CheckoutIMB, IMBCheckout
from utils.choices import TransactionStatuses, IMBTransactionTypes
from apps.checkout import models
from apps.orders import models as order_models
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
    to_orders = ReportOrdersSerializer(many=True)

    def get_amounts(self, obj):
        orders = obj.to_orders
        amounts = {
            'sum_income': 0,
            'sum_total_amount': 0,
        }
        for order in orders:
            if not order.paid:
                amounts['sum_total_amount'] += order.total_amount
            if not order.client_paid:
                amounts['sum_income'] += order.income

        return amounts


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
            'rejected',
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
                TransactionStatuses.PENDING: self.pending
            }[status](instance)

        obj = super().update(instance, validated_data)
        return obj

    @staticmethod
    def approved(instance):
        MainCheckout + instance.amount # noqa
        CheckoutIMB - instance.amount # noqa

        IMBCheckout.create_transaction(
            amount=instance.amount,
            _type=IMBTransactionTypes.AGENT_EXPENSE,
            comment=f"Arobaga chiqim"
        )

    @staticmethod
    def cancelled(instance):
        pass

    @staticmethod
    def pending(instance):
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
    income = serializers.IntegerField(read_only=True)
    payment_type = serializers.CharField(read_only=True)
    paid = serializers.BooleanField(read_only=True)


class RollbackOrderCommentSerializer(serializers.Serializer):
    comment = serializers.CharField(required=True)


class SummaryOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = order_models.Order
        fields = (
            'id',
            'client',
            'loading',
            'unloading',
            'income',
            'total_amount',
            'paid',
            'client_paid',
            'car_number',
            'comment',
            'dispatcher',
            'payment_type',
            'date',
        )
