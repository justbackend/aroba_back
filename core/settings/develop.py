from .base import *  # noqa

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
