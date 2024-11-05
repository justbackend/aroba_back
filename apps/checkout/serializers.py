from rest_framework import serializers

from . import models


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

