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
        amount = validated_data.pop('amount')
        loading = validated_data.pop('loading')
        unloading = validated_data.pop('unloading')

        obj = super().create(validated_data)
        models.ClientRoute.objects.create(client=obj, amount=amount, loading=loading, unloading=unloading)
        return obj


class ClientRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientRoute
        fields = (
            'id',
            'amount',
            'loading',
            'unloading',
            'client',
        )


class CreateClientRouteSerializer(ClientRouteSerializer):

    def validate(self, v):
        if not self.instance:
            checking = models.ClientRoute.objects.filter(
                client=v['client'], loading=v['loading'],
                unloading=v['unloading']
            )
            if checking.exists():
                raise utils.APIException('The object already exists.')
        return v

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['loading'] = utils.PointNameSerializer(obj.loading).data
        data['unloading'] = utils.PointNameSerializer(obj.unloading).data
        return data
