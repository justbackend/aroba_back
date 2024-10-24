from rest_framework import views, viewsets
from rest_framework.response import Response
from . import models, serializers


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.active_objects.all()


