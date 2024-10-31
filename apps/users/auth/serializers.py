from django.contrib.auth import authenticate
from rest_framework import serializers
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
        return self.validated_data['user'].tokens()
