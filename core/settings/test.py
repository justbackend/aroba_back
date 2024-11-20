from .base import *  # noqa

DEBUG = True

DATABASES['default']['TEST'] = {
            'MIRROR': 'default',
        }

ROOT_URLCONF = "core.urls.develop"


REST_FRAMEWORK.update(
    DEFAULT_RENDERER_CLASSES=(
        'rest_framework.renderers.JSONRenderer',
    ),
)

REST_FRAMEWORK.update(
    DEFAULT_PERMISSION_CLASSES=('utils.RolePermission',),
)
