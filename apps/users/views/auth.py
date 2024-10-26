from rest_framework import generics, status
from rest_framework.response import Response

from apps.users.serializers import auth as serializers
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from utils import customs


class LoginView(generics.GenericAPIView):
    authentication_classes = (customs.JWTAuthentication,)
    # permission_classes = ()
    serializer_class = serializers.LoginSerializer

    # @method_decorator(permission_required('users.view_role', raise_exception=True))
    def post(self, request):
        print(request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
