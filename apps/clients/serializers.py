from rest_framework import serializers

import utils
from utils.choices import *
from . import models
from apps.common.models import Point


class RouteListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    amount = serializers.IntegerField(read_only=True)
    loading = utils.PointNameSerializer(read_only=True)
    unloading = utils.PointNameSerializer(read_only=True)


class ClientSerializer(serializers.ModelSerializer):
    routes = RouteListSerializer(many=True, read_only=True)
    type = serializers.ChoiceField(choices=ClientRouteTypes.choices, write_only=True, required=True)
    amount = serializers.IntegerField(write_only=True, required=True)
    loading = serializers.PrimaryKeyRelatedField(
        write_only=True, required=True, queryset=Point.objects.all()
    )
    unloading = serializers.PrimaryKeyRelatedField(
        write_only=True, required=True, queryset=Point.objects.all()
    )

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
            'loading',
            'unloading',
            'amount',
            'type'
        )

    def create(self, validated_data):
        _type = validated_data.pop('type')
        amount = validated_data.pop('amount')
        loading = validated_data.pop('loading')
        unloading = validated_data.pop('unloading')

        obj = super().create(validated_data)
        models.ClientRoute.objects.create(client=obj, amount=amount, loading=loading, unloading=unloading, type=_type)
        return obj


class ClientRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientRoute
        fields = '__all__'
