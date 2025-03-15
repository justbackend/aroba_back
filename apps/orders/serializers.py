from rest_framework import serializers

from . import models


class FullOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'
