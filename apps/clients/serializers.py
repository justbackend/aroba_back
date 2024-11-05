from rest_framework import serializers

import utils
from . import models


class RouteListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    amount = serializers.IntegerField(read_only=True)
    loading = utils.PointNameSerializer(read_only=True)
    unloading = utils.PointNameSerializer(read_only=True)


class ClientSerializer(serializers.ModelSerializer):
    routes = RouteListSerializer(many=True, read_only=True)

    class Meta:
        model = models.Client
        fields = (
            'id',
            'name',
            'phone',
            'requisite',
            'requisite_file',
            'accounting_phone',
            'routes',
        )


class ClientRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientRoute
        fields = '__all__'

