from rest_framework import serializers
from . import models


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = '__all__'


class ClientRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientRoute
        fields = '__all__'


class CreateOrderRoutesSerializer(serializers.Serializer):
    loading_name = serializers.CharField(source='loading.name')
    loading_id = serializers.IntegerField(source='loading.id')
    unloading_name = serializers.CharField(source='unloading.name')
    unloading_id = serializers.IntegerField(source='unloading.id')
