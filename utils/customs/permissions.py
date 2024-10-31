import re

from rest_framework import permissions


class RolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if (api_list := getattr(user, 'api_list', None)) and user.is_authenticated:
            path = request.path[user.api_route_len:]

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


class IsActive(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active)
