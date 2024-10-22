from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Func, Value, BooleanField, JSONField, CharField, Q, IntegerField
from django.db.models.functions.comparison import Cast
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication as jwt_authentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.utils import get_md5_hash_password
from utils.choices import API_ROUTE_CHOICES

from apps.users.models import User as AuthUser


class JWTAuthentication(jwt_authentication):

    def authenticate(self, request):
        self.request = request
        return super(JWTAuthentication, self).authenticate(request)

    @property
    def route(self):
        path = self.request.path
        for route in API_ROUTE_CHOICES:
            if path.startswith(route[0]):
                return route[0]

    def get_user(self, validated_token: Token) -> AuthUser:
        """
        Attempts to find and return a user using the given validated token.
        """

        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        user = self.user_query(user_id, self.route)

        if not user:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")

        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")

        if api_settings.CHECK_REVOKE_TOKEN:
            if validated_token.get(
                    api_settings.REVOKE_TOKEN_CLAIM
            ) != get_md5_hash_password(user.password):
                raise AuthenticationFailed(
                    _("The user's password has been changed."), code="password_changed"
                )

        return user

    def user_query(self, user_id, route) -> AuthUser:

        return (
            AuthUser.objects
            .filter(id=user_id)
            .annotate(
                api_list=ArrayAgg(
                    Func(
                        Value('name'), 'role__modules__apis__name',
                        Value('dynamic'), 'role__modules__apis__dynamic',
                        function='JSON_BUILD_OBJECT',
                    ),
                    filter=Q(role__modules__apis__method=self.request.method, role__modules__apis__route=route)
                ),
                api_route_len=Value(len(route), output_field=IntegerField())
            )
            .first()
        )
