from itertools import groupby
from operator import itemgetter

from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, views
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from . import models, serializers


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_fields = ('routes__type',)
    search_fields = ('name', 'phone', 'accounting_phone')

    SERIALIZERS = {
        'list': serializers.ClientListSerializer,
    }

    def get_serializer_class(self):
        return self.SERIALIZERS.get(self.action, self.serializer_class)

    def get_queryset(self):
        routes_qs = (
            models.ClientRoute.objects
            .select_related('unloading', 'loading')
            .only('amount', 'type', 'loading__name', 'unloading__name', 'client_id')
        )

        return (
            models.Client.active_objects
            .prefetch_related(Prefetch('routes', queryset=routes_qs))
            .all()
        )

    def get_object(self):
        return models.Client.objects.filter(pk=self.kwargs['pk']).first()

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class ClientRouteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientRouteSerializer
    queryset = models.ClientRoute.objects.all()

