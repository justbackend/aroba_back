import os

from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.common'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            from core import scheduler
            scheduler.start_scheduler()


