from django.contrib.auth.decorators import permission_required
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F, Func, Value, TextField
from django.utils.decorators import method_decorator
from rest_framework import viewsets, generics
from rest_framework.response import Response

import utils
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


class CombinationCreateOrderRoutesListAPI(generics.GenericAPIView):

    def get(self, request, client_id, *args, **kwargs):
        routes = (
            models.ClientRoute.objects.filter(client_id=client_id)
            .values('loading_id', loading_name=F('loading__name'))
            .annotate(unloadings=ArrayAgg(
                Func(
                    Value('id'), 'unloading_id',
                    Value('name'), 'unloading__name',
                    function='JSON_BUILD_OBJECT',
                    output_field=TextField()
                ))))

        return Response(routes)
