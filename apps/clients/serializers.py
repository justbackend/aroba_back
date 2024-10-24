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
