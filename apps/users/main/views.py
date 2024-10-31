from django.contrib.postgres.aggregates import ArrayAgg
from django.http import Http404
from rest_framework import viewsets, views
from rest_framework.response import Response

from . import serializers
from .. import models


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all().order_by('-id')
    serializer_class = serializers.RoleSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = models.Module.objects.prefetch_related('permission_set').all().order_by('-id')
    serializer_class = serializers.ContentTypeSerializer


class MyPermissionsListAPI(views.APIView):

    def get(self, request, user_id: int, *args, **kwargs):
        user = models.User.objects.filter(pk=user_id).annotate(perms=ArrayAgg('user_permissions__codename')).first()
        if not user:
            raise Http404
        return Response(user.perms)
