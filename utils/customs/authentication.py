from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions.comparison import Cast
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication as jwt_authentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.utils import get_md5_hash_password

from apps.users.models import User as AuthUser, API, Module
from django.db.models import Prefetch, OuterRef, Func, Value, BooleanField, JSONField, CharField


class JWTAuthentication(jwt_authentication):

    def authenticate(self, request):
        self.request = request
        return super(JWTAuthentication, self).authenticate(request)

    def get_user(self, validated_token: Token) -> AuthUser:
        """
        Attempts to find and return a user using the given validated token.
        """

        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        user = (
            AuthUser.objects
            .filter(id=user_id)
            .annotate(
                api_data=ArrayAgg(
                    Cast(
                        Func(
                            Value('name'), 'role__modules__apis__name',
                            Value('route'), 'role__modules__apis__route',
                            Value('method'), 'role__modules__apis__method',
                            Value('dynamic'), Cast('role__modules__apis__dynamic', output_field=BooleanField()),
                            function='JSON_BUILD_OBJECT',
                            output_field=JSONField()
                        ),
                        output_field=CharField()
                    )
                )
            )
            .first()
        )

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
