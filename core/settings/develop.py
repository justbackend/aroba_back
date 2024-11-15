
from .base import *  # noqa


DEBUG = True
CELERY_TASK_ALWAYS_EAGER = True

INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
REST_FRAMEWORK.update(
    DEFAULT_PERMISSION_CLASSES=('utils.RolePermission',),
)

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}
ROOT_URLCONF = "core.urls.develop"


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
