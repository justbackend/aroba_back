from rest_framework import serializers
from . import models


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = '__all__'


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Point
        fields = '__all__'
