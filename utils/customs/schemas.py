from drf_spectacular.extensions import OpenApiAuthenticationExtension
from utils.customs import JWTAuthentication


class CustomJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'utils.customs.JWTAuthentication'  # To'liq yo'lni tekshiring
    name = 'CustomJWT'
    priority = 1

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
