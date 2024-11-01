from rest_framework import serializers


class UserNameSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)


class PointNameSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)


class PointLonLatSerializer(PointNameSerializer):
    lon = serializers.CharField(read_only=True)
    lat = serializers.CharField(read_only=True)


class ClientNameSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
