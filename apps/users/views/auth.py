from rest_framework import generics, status
from rest_framework.response import Response

from apps.users.serializers import auth as serializers
from django.core.cache import cache


class LoginView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        print(cache.get('salom_1'))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
