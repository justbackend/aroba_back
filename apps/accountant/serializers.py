from rest_framework import serializers
from apps.clients import models as client_models


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


class InvoiceOrdersSerializer(serializers.Serializer):
    pass