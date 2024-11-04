from rest_framework import generics, status, views
from rest_framework.response import Response

from utils.customs.authentication import PayloadAuthentication
from . import serializers
from .. import models, utils


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
        profile_data = models.User.profile_data(request.auth['user_id'])
        if profile_data.get("photo"):
            profile_data["photo"] = request.build_absolute_uri(profile_data["photo"])
        return Response(profile_data)


class MyPermissionsListAPI(views.APIView):
    authentication_classes = (PayloadAuthentication,)

    def get(self, request, *args, **kwargs):
        return Response(utils.get_user_perms(request.auth['user_id']))
