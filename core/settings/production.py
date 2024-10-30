from .base import *  # noqa

###################################################################
# General
###################################################################

DEBUG = True

###################################################################
# Django security
###################################################################

"""
IF YOU WANT SET CSRF_TRUSTED_ORIGINS = ["*"] THEN YOU SHOULD SET:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
"""

CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = [
    "https://example.com"
]

###################################################################
# CORS
###################################################################

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]


REST_FRAMEWORK.update(
    DEFAULT_RENDERER_CLASSES=(
        'rest_framework.renderers.JSONRenderer',
    ),
)

ROOT_URLCONF = "core.urls.production"
