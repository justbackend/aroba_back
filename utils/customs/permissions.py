import re
from django.core.cache import cache
from rest_framework import permissions
from apps.users import models
from utils.choices import APIRoutes


def get_apis_perm(user) -> list:
    data = cache.get(f'apis_perm_{user.id}')
    if data is None:
        apis = models.APIRoute.objects.filter(actions__users=user).distinct()
        data = list(
            map(lambda api: dict(dynamic=api.dynamic, name=api.name, method=api.method, route=api.route), apis)
        )
        cache.set(f'apis_perm_{user.id}', data)

    return data


class RolePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user and user.is_authenticated:
            api_list, api_route_len = self.get_filtered_perms_and_route(request)
            path = request.path[api_route_len:]

            for api_info in api_list:

                if int(api_info['dynamic']):
                    pattern = f"^{api_info['name'].replace('$', '[^/]+')}$"
                    if re.match(pattern, path):
                        return True
                else:
                    api_info['name'] = api_info['name'] or ''
                    if api_info['name'] == path:
                        return True

        return False

    @classmethod
    def get_filtered_perms_and_route(cls, request):
        data = get_apis_perm(request.user)
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
