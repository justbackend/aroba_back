from rest_framework import serializers
from .. import models


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Module
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'

