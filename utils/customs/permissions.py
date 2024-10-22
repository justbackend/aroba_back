import json
from rest_framework import permissions
import re


class RolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        path = request.path[user.api_route_len:]

        if user.api_list:
            for api_info in user.api_list:

                if int(api_info['dynamic']):
                    pattern = f"^{api_info['name'].replace('<id>', '[^/]+')}$"
                    if re.match(pattern, path):
                        return True
                else:
                    if api_info['name'] == path:
                        return True

        return False
