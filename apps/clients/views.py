from rest_framework import viewsets
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from . import models, serializers


@method_decorator(permission_required('users.view_role', raise_exception=True), name='dispatch')
class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientSerializer
    queryset = models.Client.active_objects.all()

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()



class ClientRouteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClientRouteSerializer
    queryset = models.ClientRoute.objects.all()
