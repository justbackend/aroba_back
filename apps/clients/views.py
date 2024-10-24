from rest_framework import viewsets

from . import models, serializers


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.objects.all()

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class ClientRouteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientRouteSerializer
    queryset = models.ClientRoute.objects.all()
