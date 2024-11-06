from rest_framework import serializers


class ClientSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    phone = serializers.CharField()
    accounting_phone = serializers.CharField()
    requisite = serializers.CharField()
    requisite_file = serializers.FileField()


class AccountantOrdersSerializer(serializers.Serializer):
    loading = serializers.CharField(source='loading.name', read_only=True)
    unloading = serializers.CharField(source='unloading.name', read_only=True)
    code = serializers.CharField()
    total_amount = serializers.IntegerField()
    client = ClientSerializer()


class FinishedOrdersSerializer(serializers.Serializer):
    client_id = serializers.IntegerField(source='client.id')
    client_name = serializers.CharField(source='client.name')
    date = serializers.DateField()
    loading = serializers.CharField(source='loading.name')
    unloading = serializers.CharField(source='unloading.name')
    car_number = serializers.CharField()
    total_amount = serializers.IntegerField()
