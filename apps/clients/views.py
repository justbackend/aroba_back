from rest_framework import viewsets, views
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from rest_framework.response import Response

from . import models, serializers


# @method_decorator(permission_required('users.view_role', raise_exception=True), name='dispatch')
class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.active_objects.all()

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()

    @method_decorator(permission_required('app.view_client', raise_exception=True))
    def list(self, request, *args, **kwargs):
        return super(ClientViewSet, self).list(request, *args, **kwargs)


class ClientRouteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientRouteSerializer
    queryset = models.ClientRoute.objects.all()


class Salom(views.APIView):

    @method_decorator(permission_required('app.salom', raise_exception=True))
    def get(self, request):
        return Response({})
