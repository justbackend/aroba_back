from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"

    def ready(self):

        """
        Cannot be deleted  the imports
        """

        from . import signals
        from utils.customs.schemas import JWTAuthenticationScheme, PayloadAuthenticationScheme
