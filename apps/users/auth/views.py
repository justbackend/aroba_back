from rest_framework import generics, status, views
from rest_framework.response import Response
from utils.customs.authentication import PayloadAuthentication

from . import serializers


class LoginView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileView(views.APIView):
    authentication_classes = (PayloadAuthentication,)
    permission_classes = ()

    def get(self, request):
        return Response({'payload': request.auth})
