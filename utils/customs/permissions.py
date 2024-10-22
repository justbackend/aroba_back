import json
from rest_framework import permissions
import re


class RolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        path = request.path[len(user.api_route):]

        if user.api_list:
            for api_data in user.api_list:
                api_info = json.loads(api_data)

                if api_info['dynamic']:
                    pattern = f"^{api_info['name'].replace('<id>', '[^/]+')}$"
                    if re.match(pattern, path):
                        return True
                else:
                    if api_info['name'] == path:
                        return True

        return False
