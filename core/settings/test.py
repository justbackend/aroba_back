from .base import *  # noqa

DEBUG = True

DATABASES['default']['TEST'] = {
            'MIRROR': 'default',
        }

ROOT_URLCONF = "core.urls.develop"
