import re

from django.conf import settings
from django.core.cache import cache
from rest_framework import permissions

from apps.users.utils import get_user_perms
from utils.choices import APIRoutes


class RolePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if user and user.is_authenticated:

            if user.is_superuser:
                return True

            if self.has_perm(request):
                return True

            perms, route, path = self.get_filtered_perms_and_route(request)

            if not route:
                return False

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
        route = cls.get_route(request)
        path = request.path[len(route):]
        perms = get_user_perms(request, route=route, path=path)
        return perms, route, path

    @staticmethod
    def get_route(request):
        path = request.path
        for route in APIRoutes.choices:
            if path.startswith(route[0]):
                return route[0]

    @staticmethod
    def has_perm(request) -> bool | None:
        user = request.user
        has_perms = cache.get(f'has_perms_{user.id}')
        if isinstance(has_perms, dict):
            return bool(has_perms.get(request.path))

    @staticmethod
    def set_has_perm(request, _type: bool):
        user = request.user
        has_perms = cache.get(f'has_perms_{user.id}')

        if isinstance(has_perms, dict):
            has_perms[request.path] = _type
            cache.set(f'has_perms_{user.id}', has_perms, 3600)
            return

        cache.set(f'has_perms_{user.id}', {request.path: _type}, 3600)



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
