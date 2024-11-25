from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from . import serializers
from .. import models


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all().order_by('-id')
    serializer_class = serializers.RoleSerializer
    pagination_class = None


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = models.Module.objects.prefetch_related('actions').all().order_by('-id')
    serializer_class = serializers.ModuleSerializer
    pagination_class = None


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CreateUserSerializer
    queryset = models.User.objects.filter(is_superuser=False)
    pagination_class = None
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return models.User.objects.filter(id=self.kwargs['pk']).first()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class SectionViewSet(viewsets.ModelViewSet):
    queryset = (
        models.Section.objects
        .prefetch_related('modules', 'modules__actions', 'modules__actions__apis')
        .all().order_by('order')
    )
    serializer_class = serializers.SectionSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset

        actions = user.actions.all()
        return self.queryset.filter(modules__actions__in=actions).distinct()
