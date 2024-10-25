# from django.urls import path, include
# from core.urls import urlpatterns

from .base import *  # noqa

# urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))


DEBUG = True
CELERY_TASK_ALWAYS_EAGER = True

INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
REST_FRAMEWORK.update(
    DEFAULT_PERMISSION_CLASSES=('rest_framework.permissions.AllowAny',),
)

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}
ROOT_URLCONF = "core.urls.develop"
