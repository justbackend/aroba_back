from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets, generics

import utils
from . import models, serializers


# @utils.permission_required_cls(perm='test.test_view', methods=('list',))
class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.active_objects.all()

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class ClientRouteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientRouteSerializer
    queryset = models.ClientRoute.objects.all()


class CreateOrderRoutes(generics.ListAPIView):
    serializer_class = serializers.CreateOrderRoutesSerializer
    filter_backends = ()
    pagination_class = None

    def get_queryset(self):
        return (
            models.ClientRoute.objects.filter(client_id=self.kwargs['client_id'])
            .select_related('unloading', 'loading')
            .only('id', 'unloading__name', 'loading__name', 'loading_id', 'unloading_id')
        )
