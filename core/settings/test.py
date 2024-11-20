from .base import *  # noqa

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aroba_test',
        'USER': 'aroba_test',
        'PASSWORD': 'aroba_test',
        'HOST': 'localhost',
        'PORT': '5432',
        "ATOMIC_REQUESTS": True,
        'TEST': {
            'MIRROR': 'default',
        },
    }
}

ROOT_URLCONF = "core.urls.develop"
