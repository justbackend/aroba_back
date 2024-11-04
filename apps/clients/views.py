from itertools import groupby
from operator import itemgetter

from django.db.models import Prefetch
from django_filters import filters
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
            .all()
        )
        return (
            models.Client.active_objects
            .prefetch_related(Prefetch('routes', queryset=routes_qs))
            .all().distinct()
        )

    def get_object(self):
        return models.Client.objects.filter(pk=self.kwargs['pk']).first()

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class ClientRouteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientRouteSerializer
    queryset = models.ClientRoute.objects.all()


class CombinationCreateOrderRoutesListAPI(views.APIView):

    def get(self, request, client_id, *args, **kwargs):
        routes_list = (
            models.ClientRoute.objects.filter(client_id=client_id)
            .values('loading_id', 'loading__name', 'unloading_id', 'unloading__name')
        )

        routes_grouped = []
        for key, group in groupby(sorted(routes_list, key=itemgetter('loading_id')),
                                  key=itemgetter('loading_id', 'loading__name')):
            loading_id, loading_name = key
            unloadings = [
                {"id": g['unloading_id'], "name": g['unloading__name']}
                for g in group
            ]
            routes_grouped.append({
                "loading_id": loading_id,
                "loading_name": loading_name,
                "unloadings": unloadings
            })

        return Response(routes_grouped)
