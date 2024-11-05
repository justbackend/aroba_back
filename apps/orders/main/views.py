from itertools import groupby
from operator import itemgetter

from rest_framework import generics, views
from rest_framework.response import Response

import utils
from apps.clients import models as clients_models
from . import serializers


class CreateOrderView(generics.CreateAPIView):
    serializer_class = serializers.CreateOrderSerializer


class ClientsListView(generics.ListAPIView):
    serializer_class = utils.create_serializer({'id': int, 'name': str})
    queryset = clients_models.Client.active_objects.all()
    pagination_class = None


class CombinationCreateOrderRoutesListAPI(views.APIView):

    def get(self, request, client_id, *args, **kwargs):

        routes_list = (
            clients_models.ClientRoute.objects.filter(client_id=client_id, )
            .values('loading_id', 'loading__name', 'unloading_id', 'unloading__name')
        )

        if _type := self.request.query_params.get('type', None):
            routes_list = routes_list.filter(type=_type)

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
