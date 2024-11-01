from itertools import groupby
from operator import itemgetter

from rest_framework import viewsets, views
from rest_framework.response import Response

from . import models, serializers


# @utils.permission_required_cls(perm='test.test_view', methods=('list',))
class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.active_objects.all()
    pagination_class = None

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
