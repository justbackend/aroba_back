from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models import User
import utils


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise utils.APIException("Invalid username or password")

        data['user'] = user
        return data

    def to_representation(self, instance):
        return dict(user_id=self.validated_data['user'].id, **self.validated_data['user'].tokens())


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'phone',
            'chat_id',
        )


