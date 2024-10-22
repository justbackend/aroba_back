from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CustomJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'utils.customs.JWTAuthentication'  # To'liq yo'lni tekshiring
    name = 'JWTAuthentication'
    priority = 1

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
