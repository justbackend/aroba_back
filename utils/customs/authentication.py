from typing import Union

from django.contrib.postgres.aggregates import ArrayAgg
from django.core.cache import cache
from django.db.models import Func, Value, TextField
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication as jwt_authentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import Token, AccessToken
from rest_framework_simplejwt.utils import get_md5_hash_password

from apps.users.models import User as AuthUser
from utils.choices import APIRoutes


class JWTAuthentication(jwt_authentication):
    """
        An authentication plugin that authenticates requests through a JSON web
        token provided in a request header.
    """

    def __init__(self):
        self.request = None

    def authenticate(self, request):
        setattr(self, 'request', request)
        return super(JWTAuthentication, self).authenticate(request)

    @property
    def route(self):
        path = self.request.path
        for route in APIRoutes.choices:
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

        user = self.user_query(user_id)

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

    def user_query(
            self,
            user_id: int,
    ) -> Union['AuthUser', None]:

        perms = cache.get(f'apis_perm_{user_id}')
        if perms:
            return AuthUser.objects.filter(id=user_id).first()

        elif not perms:
            user = (
                AuthUser.objects
                .filter(id=user_id)
                .annotate(
                    perms=ArrayAgg(
                        Func(
                            Value('name'), 'actions__apis__name',
                            Value('dynamic'), 'actions__apis__dynamic',
                            Value('method'), 'actions__apis__method',
                            Value('route'), 'actions__apis__route',
                            function='JSON_BUILD_OBJECT',
                            output_field=TextField()
                        ),
                    ),
                )
                .first()
            )

            if user:
                cache.set(f'apis_perm_{user_id}', user.perms)
                delattr(user, 'perms')
                return user


class PayloadAuthentication(BaseAuthentication):
    """
    An authentication plugin that authenticates requests through a JSON web
    """

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        try:
            auth_scheme, token = auth_header.split(' ')
        except ValueError:
            raise AuthenticationFailed(_('Invalid Authorization header format. Expected "Bearer <token>"'))

        if auth_scheme.lower() != 'bearer':
            raise AuthenticationFailed(_('Authorization scheme must be Bearer'))

        try:
            access_token = AccessToken(token)
            payload = access_token.payload
        except Exception as e:
            raise AuthenticationFailed(_('Invalid or expired token'))

        return None, payload

    def authenticate_header(self, request):
        return 'Bearer realm="api"'
