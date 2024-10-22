from rest_framework import views, response
from utils.customs import RolePermission


class SalomView(views.APIView):
    permission_classes = (RolePermission,)

    def get(self, request, *args, **kwargs):
        return response.Response({})
