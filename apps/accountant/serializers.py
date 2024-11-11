from rest_framework import serializers

import utils
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


class FinishedOrdersSerializer(serializers.Serializer):
    client_name = serializers.CharField(source='client.name')
    date = serializers.DateField()
    loading = serializers.CharField(source='loading.name')
    unloading = serializers.CharField(source='unloading.name')
    car_number = serializers.CharField()
    total_amount = serializers.IntegerField()


class ChildOrders(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    loading_name = serializers.CharField()
    unloading_name = serializers.CharField()
    car_number = serializers.CharField()


class ParentInvoice(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    status = serializers.CharField()
    to_orders = ChildOrders(many=True)


class InvoiceOrdersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    inn = serializers.CharField()
    accounting_phone = serializers.CharField()
    invoices = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.now = utils.now()

    def get_invoices(self, client):
        data = [self.collect_empty_orders(client.to_orders)] + client.to_invoices
        return ParentInvoice(instance=data, many=True).data

    def collect_empty_orders(self, orders):
        invoice = models.AccountantInvoice(
            id=-1,
            created_at=self.now,
            updated_at=self.now,
            status=None
        )
        setattr(invoice, 'to_orders', orders)

        return invoice
