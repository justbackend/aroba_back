from .base import *  # noqa

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_aroba',
        'USER': 'test_aroba',
        'PASSWORD': 'test_aroba',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

ROOT_URLCONF = "core.urls.develop"
