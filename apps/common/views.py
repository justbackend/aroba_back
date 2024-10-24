from rest_framework import viewsets

from . import models, serializers


class RegionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RegionSerializer
    queryset = models.Region.objects.all()


class PointViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PointSerializer
    queryset = models.Point.objects.all()

