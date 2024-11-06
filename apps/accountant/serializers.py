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

