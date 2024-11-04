import re
from django.core.cache import cache
from rest_framework import permissions
from .choices import APIRoutes


class RolePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user and user.is_authenticated:
            perms, api_route_len = self.get_filtered_perms_and_route(request)
            path = request.path[api_route_len:]

            for perm in perms:

                if perm['dynamic']:
                    pattern = f"^{perm['name'].replace('$', '[^/]+')}$"
                    if re.match(pattern, path):
                        return True
                else:
                    perm['name'] = perm['name'] or ''
                    if perm['name'] == path:
                        return True

        return False

    @classmethod
    def get_filtered_perms_and_route(cls, request):
        data = cache.get(f'apis_perm_{request.user.id}')
        route = cls.get_route(request)
        return tuple(filter(lambda perm: perm['method'] == request.method and perm['route'] == route, data)), len(route)

    @staticmethod
    def get_route(request):
        path = request.path
        for route in APIRoutes.choices:
            if path.startswith(route[0]):
                return route[0]


class IsActive(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active)
