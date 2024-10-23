from rest_framework import views, viewsets, generics, status
from rest_framework.response import Response

from utils.customs import RolePermission
from . import serializers, models


class LoginView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SalomView(views.APIView):
    permission_classes = (RolePermission,)

    def get(self, request, *args, **kwargs):
        return Response({})
