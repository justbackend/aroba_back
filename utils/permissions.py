import re

from rest_framework import permissions

from apps.users.utils import get_user_perms
from .choices import APIRoutes
from django.core.cache import cache


class RolePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user and user.is_authenticated:

            if self.has_perm(request):
                return True

            perms, api_route_len = self.get_filtered_perms_and_route(request)
            path = request.path[api_route_len:]

            for perm in perms:

                if perm['dynamic']:
                    pattern = f"^{perm['name'].replace('$', '[^/]+')}$"
                    if re.match(pattern, path):
                        self.set_has_perm(request)
                        return True
                else:
                    perm['name'] = perm['name'] or ''
                    if perm['name'] == path:
                        self.set_has_perm(request)
                        return True

        return False

    @classmethod
    def get_filtered_perms_and_route(cls, request):
        data = get_user_perms(request.user.id)
        route = cls.get_route(request)
        return tuple(filter(lambda perm: perm['method'] == request.method and perm['route'] == route, data)), len(route)

    @staticmethod
    def get_route(request):
        path = request.path
        for route in APIRoutes.choices:
            if path.startswith(route[0]):
                return route[0]

    @staticmethod
    def has_perm(request) -> bool:
        user = request.user
        has_perms = cache.get(f'has_perm_{user.id}')
        return isinstance(has_perms, dict) and has_perms.get(request.path)

    @staticmethod
    def set_has_perm(request):
        user = request.user
        has_perms = cache.get(f'has_perm_{user.id}')

        if isinstance(has_perms, dict):
            has_perms[request.path] = True
            cache.set(f'has_perm_{user.id}', has_perms)
            return

        cache.set(f'has_perm_{user.id}', {request.path: True})


class IsActive(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active)


class PayloadPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.auth)
