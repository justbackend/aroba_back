from rest_framework import views, generics, status, viewsets
from rest_framework.response import Response

from utils.customs import RolePermission
from .. import models
from . import serializers


class SalomView(views.APIView):
    permission_classes = (RolePermission,)

    def get(self, request, *args, **kwargs):
        return Response({})


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer



class ModuleViewSet(viewsets.ModelViewSet):
    queryset = models.Module.objects.all()
    serializer_class = serializers.ModuleSerializer
