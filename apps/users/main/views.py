from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from utils.permissions import RolePermission
from . import serializers
from .. import models


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all().order_by('-id')
    serializer_class = serializers.RoleSerializer
    pagination_class = None


class ModuleViewSet(viewsets.ModelViewSet):
    permission_classes = (RolePermission,)
    queryset = models.Module.objects.prefetch_related('actions').all().order_by('-id')
    serializer_class = serializers.ModuleSerializer
    pagination_class = None


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CreateUserSerializer
    queryset = models.User.objects.all()
    pagination_class = None
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return models.User.objects.filter(id=self.kwargs['pk']).first()
