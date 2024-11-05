from rest_framework import serializers


class ReportSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
