from rest_framework import viewsets

from . import models, serializers


class RegionViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.RegionSerializer
    queryset = models.Region.objects.all()
    pagination_class = None


class PointViewSet(viewsets.ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.PointSerializer
    queryset = models.Point.active_objects.all()
    pagination_class = None

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
