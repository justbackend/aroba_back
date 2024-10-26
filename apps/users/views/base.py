from rest_framework import viewsets
from apps.users.serializers import base as serializers
from .. import models


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all().order_by('-id')
    serializer_class = serializers.RoleSerializer


class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = models.ContentType.objects.all().order_by('-id')
    serializer_class = serializers.ContentTypeSerializer
