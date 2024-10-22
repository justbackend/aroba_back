# from drf_spectacular.extensions import OpenApiAuthenticationExtension
# from .authentication import JWTAuthentication


# class CustomJWTAuthenticationScheme(OpenApiAuthenticationExtension):
#     target_class = 'utils.authentication.JWTAuthentication'  # to'liq yo'l
#     name = 'CustomJWT'  # autentifikatsiya nomi
#     priority = 1  # prioritet
#
#     def get_security_definition(self, auto_schema):
#         return {
#             'type': 'http',
#             'scheme': 'bearer',
#             'bearerFormat': 'JWT',
#         }


# OpenApiAuthenticationExtension.target_class = 'utils.authentication.JWTAuthentication'
