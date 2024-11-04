from rest_framework import serializers
from . import models
import utils


class RouteListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    amount = serializers.IntegerField(read_only=True)
    loading = utils.PointNameSerializer(read_only=True)
    unloading = utils.PointNameSerializer(read_only=True)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = '__all__'


class ClientListSerializer(serializers.ModelSerializer):
    routes = RouteListSerializer(many=True)

    class Meta:
        model = models.Client
        fields = (
            'id',
            'name',
            'phone',
            'accounting_phone',
            'requisite_file',
            'requisite',
            'routes'
        )


class ClientRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientRoute
        fields = '__all__'


class CreateOrderRoutesSerializer(serializers.Serializer):
    loading_name = serializers.CharField(source='loading.name')
    loading_id = serializers.IntegerField(source='loading.id')
    unloading_name = serializers.CharField(source='unloading.name')
    unloading_id = serializers.IntegerField(source='unloading.id')
