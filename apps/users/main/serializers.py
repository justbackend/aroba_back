from rest_framework import serializers

from utils.utility import clear_users_perms
from .. import models


class APIRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.APIRoute
        fields = '__all__'


class ActionNameSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    apis = APIRouteSerializer(many=True, read_only=True)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    actions = ActionNameSerializer(many=True)

    class Meta:
        model = models.Module
        fields = ('id', 'name', 'actions')


class SectionSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True)

    class Meta:
        model = models.Section
        fields = ('id', 'name', 'modules')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = ('id', 'name', 'actions')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.actions.set(validated_data['actions'])
        instance.save()
        return instance


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id',
            'last_name',
            'first_name',
            'username',
            'password',
            'roles',
            'phone',
            'photo',
        )

        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def to_internal_value(self, data):
        mutable_data = data.copy()

        if 'roles[]' in mutable_data:
            mutable_data.setlist('roles', mutable_data.getlist('roles[]'))
            del mutable_data['roles[]']

        return super().to_internal_value(mutable_data)
