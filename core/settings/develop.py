from .base import *  # noqa

DEBUG = True
CELERY_TASK_ALWAYS_EAGER = True

INSTALLED_APPS += ['debug_toolbar', ]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
REST_FRAMEWORK.update(
    DEFAULT_PERMISSION_CLASSES=('rest_framework.permissions.AllowAny',),
    DEFAULT_RENDERER_CLASSES=('rest_framework.renderers.BrowsableAPIRenderer',),
)

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}
