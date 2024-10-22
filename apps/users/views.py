from rest_framework import views, generics, viewsets, response
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.customs.permissions import RolePermission


class SalomView(views.APIView):
    permission_classes = (RolePermission,)

    def get(self, request, *args, **kwargs):
        return response.Response({})
