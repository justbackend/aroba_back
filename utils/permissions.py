import re

from rest_framework import permissions

from apps.users.utils import get_user_perms
from .choices import APIRoutes
from django.core.cache import cache
from django.conf import settings


class RolePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user and user.is_authenticated:

            if user.is_superuser:
                return True

            if self.has_perm(request):
                return True

            perms, route = self.get_filtered_perms_and_route(request)

            if not route:
                return False
            route_len = len(route)

            path = request.path[route_len:]

            for perm in perms:

                if perm['dynamic']:
                    pattern = f"^{perm['name'].replace('$', '[^/]+')}$"
                    if re.match(pattern, path):
                        return True
                else:
                    perm['name'] = perm['name'] or ''
                    if perm['name'] == path:
                        self.set_has_perm(request, True)
                        return True

        return False

    @classmethod
    def get_filtered_perms_and_route(cls, request):
        data = get_user_perms(request.user.id)
        route = cls.get_route(request)
        return tuple(filter(lambda perm: perm['method'] == request.method and perm['route'] == route, data)), route

    @staticmethod
    def get_route(request):
        path = request.path
        for route in APIRoutes.choices:
            if path.startswith(route[0]):
                return route[0]

    @staticmethod
    def has_perm(request) -> bool:
        user = request.user
        has_perms = cache.get(f'has_perms_{user.id}')
        if isinstance(has_perms, dict):
            return has_perms.get(request.path)

    @staticmethod
    def set_has_perm(request, _type: bool):
        user = request.user
        has_perms = cache.get(f'has_perms_{user.id}')

        if isinstance(has_perms, dict):
            has_perms[request.path] = _type
            cache.set(f'has_perms_{user.id}', has_perms)
            return

        cache.set(f'has_perms_{user.id}', {request.path: _type})


class IsActive(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active)


class PayloadPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.auth)


class IMBPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user == settings.IMB_SECRETS['user_id']
