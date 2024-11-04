from rest_framework import serializers
from . import models
from apps.common import models as common_models
import utils
from utils import choices


class RouteListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    amount = serializers.IntegerField(read_only=True)
    loading = utils.PointNameSerializer(read_only=True)
    unloading = utils.PointNameSerializer(read_only=True)


class ClientSerializer(serializers.ModelSerializer):
    loading = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=common_models.Point.active_objects.all()
    )
    unloading = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=common_models.Point.active_objects.all()
    )
    amount = serializers.IntegerField(required=True, min_value=1, write_only=True)
    type = serializers.ChoiceField(choices=choices.ClientRouteTypes.choices)

    class Meta:
        model = models.Client
        fields = (
            'id',
            'name',
            'phone',
            'requisite',
            'requisite_file',
            'accounting_phone',
            'loading',
            'unloading',
            'type',
            'amount'
        )

    def create(self, validated_data):
        print(validated_data)
        loading = validated_data.pop('loading')
        unloading = validated_data.pop('unloading')
        amount = validated_data.pop('amount')
        _type = validated_data.pop('type')
        obj = models.Client(**validated_data)

        models.ClientRoute.objects.create(loading=loading, unloading=unloading, amount=amount, type=_type)
        return obj


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
