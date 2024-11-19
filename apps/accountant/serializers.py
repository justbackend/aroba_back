from rest_framework import serializers

import utils
from utils.choices import *
from apps.clients import models as client_models
from . import models


class TransClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = client_models.Client
        fields = (
            'id',
            'name',
            'requisite',
            'requisite_file',
            'customer',
            'phone',
            'accounting_phone',
            'inn',
        )
        extra_kwargs = {
            'accounting_phone': {'required': True},
            'customer': {'required': True},
            'inn': {'required': True},
        }


class FinishedOrdersSerializer(serializers.Serializer):
    client_name = serializers.CharField(source='client.name')
    date = serializers.DateField()
    loading = serializers.CharField(source='loading.name')
    unloading = serializers.CharField(source='unloading.name')
    car_number = serializers.CharField()
    income = serializers.IntegerField()
    client_paid = serializers.BooleanField()


class ChildOrdersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField()
    income = serializers.DecimalField(max_digits=15, decimal_places=2)
    loading_name = serializers.CharField()
    unloading_name = serializers.CharField()
    car_number = serializers.CharField()
    status = serializers.IntegerField()
    invoice_id = serializers.IntegerField()


class ParentInvoiceSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    status = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=30, decimal_places=2)
    to_orders = ChildOrdersSerializer(many=True)


class InvoiceOrdersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    inn = serializers.CharField()
    customer = serializers.CharField()
    accounting_phone = serializers.CharField()
    amounts = serializers.SerializerMethodField()
    invoices = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.now = utils.now()

    def get_invoices(self, client):

        data = client.to_invoices
        if client.to_orders:
            data = [self.collect_empty_orders(client.to_orders)] + client.to_invoices

        return ParentInvoiceSerializers(instance=data, many=True).data

    def collect_empty_orders(self, orders):
        invoice = models.AccountantInvoice(
            id=-1,
            created_at=self.now,
            updated_at=self.now,
            status=None,
            total_amount=self.amounts['unsent']
        )
        setattr(invoice, 'to_orders', orders)

        return invoice

    def get_amounts(self, client):
        self.amounts = {
            InvoiceStatuses.PENDING: 0,
            InvoiceStatuses.APPROVED: 0,
        }
        for invoice in client.to_invoices:
            self.amounts[invoice.status] += invoice.total_amount

        self.amounts['unsent'] = sum(map(lambda x: x.income, client.to_orders))

        return self.amounts


class CreateInvoiceSerializer(serializers.Serializer):
    orders = serializers.ListField(child=serializers.IntegerField(min_value=1), required=True)


class UpdateInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountantInvoice
        fields = (
            'id',
            'status',
        )

    def update(self, instance, validated_data):
        methods = {
            InvoiceStatuses.APPROVED: self.approved,
            InvoiceStatuses.PENDING: self.pending,
            InvoiceStatuses.CANCELLED: self.cancelled,
        }

        status = validated_data.get('status', instance.status)
        instance.status = status
        instance.save()
        methods[status](instance)
        return instance

    @staticmethod
    def approved(instance):
        instance.orders.all().update(client_paid=True)

    @staticmethod
    def pending(instance):
        pass

    @staticmethod
    def cancelled(instance):
        instance.orders.all().update(invoice=None, client_paid=False)
