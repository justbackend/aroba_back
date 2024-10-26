from rest_framework import serializers
from .. import models


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContentType
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'

