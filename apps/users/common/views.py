from rest_framework import views, generics, status
from rest_framework.response import Response

from utils.customs import RolePermission


class SalomView(views.APIView):
    permission_classes = (RolePermission,)

    def get(self, request, *args, **kwargs):
        return Response({})
