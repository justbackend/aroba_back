from rest_framework import generics, status, views
from rest_framework.response import Response

from utils.customs.authentication import PayloadAuthentication
from . import serializers
from .. import models, utils
from utils.permissions import PayloadPermission


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
    permission_classes = (PayloadPermission,)

    def get(self, request):
        if not (user_id := request.auth.get('user_id')):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        profile_data = models.User.profile_data(user_id)
        if profile_data.get("photo"):
            profile_data["photo"] = request.build_absolute_uri(profile_data["photo"])
        return Response(profile_data)


class MyPermissionsListAPI(views.APIView):
    authentication_classes = (PayloadAuthentication,)
    permission_classes = (PayloadPermission,)

    def get(self, request, *args, **kwargs):
        return Response(utils.get_user_perms(request.auth['user_id']))
