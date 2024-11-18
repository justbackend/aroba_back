from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from . import models, serializers


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientSerializer
    search_fields = ('name', 'phone', 'accounting_phone')

    routes_qs = (
        models.ClientRoute.objects
        .select_related('unloading', 'loading')
        .only('amount', 'type', 'loading__name', 'unloading__name', 'client_id')
    )

    def get_queryset(self):
        _type = self.request.query_params.get('routes__type')
        return (
            models.Client.active_objects
            .prefetch_related(Prefetch('routes', queryset=self.routes_qs.filter(type=_type)))
            .all()
        )

    def get_object(self):
        return (
            models.Client.objects
            .prefetch_related(Prefetch('routes', queryset=self.routes_qs))
            .filter(pk=self.kwargs['pk']).first()
        )

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class ClientRouteViewSet(viewsets.ModelViewSet):
    queryset = models.ClientRoute.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ClientRouteSerializer
        return serializers.CreateClientRouteSerializer
