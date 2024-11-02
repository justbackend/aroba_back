from django.contrib.postgres.aggregates import ArrayAgg
from django.http import Http404
from rest_framework import viewsets, views
from rest_framework.response import Response

from utils import RolePermission
from . import serializers
from .. import models
from django.core.cache import cache


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all().order_by('-id')
    serializer_class = serializers.RoleSerializer
    pagination_class = None


class ModuleViewSet(viewsets.ModelViewSet):
    permission_classes = (RolePermission,)
    queryset = models.Module.objects.prefetch_related('actions').all().order_by('-id')
    serializer_class = serializers.ContentTypeSerializer
    pagination_class = None


class MyPermissionsListAPI(views.APIView):

    def get(self, request, user_id: int, *args, **kwargs):
        return Response(cache.get(f'apis_perm_{user_id}'))

