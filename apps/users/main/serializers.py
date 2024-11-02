from rest_framework import serializers
from .. import models


class ActionNameSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    actions = ActionNameSerializer(many=True)

    class Meta:
        model = models.Module
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'
