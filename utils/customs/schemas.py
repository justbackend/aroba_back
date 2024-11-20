from drf_spectacular.extensions import OpenApiAuthenticationExtension


class JWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'utils.customs.JWTAuthentication'
    name = 'JWTAuthentication'
    priority = 1

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }


class PayloadAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'utils.customs.PayloadAuthentication'
    name = 'JWTAuthentication'
    priority = 1

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }


class IMBAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'utils.customs.IMBAuthentication'
    name = 'Auth'
    priority = 1

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Custom Auth header in the format: user_id:token:timestamp'
        }

