from rest_framework import serializers
from .. import models


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = '__all__'


class ContentTypeSerializer(serializers.ModelSerializer):
    permission_set = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Module
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'
