__all__ = (
    'EXTERNAL_USERS',
)

from dataclasses import dataclass
from functools import cached_property
from django.conf import settings
from .models import User


@dataclass(slots=True)
class ExternalUsers:

    @cached_property
    def imb_user(self):
        data = dict(
            username=settings.IMB_USER_SECRETS['username'],
            first_name='IMB TRUCK',
            last_name='IMB TRUCK',
            is_superuser=True
        )
        user = User.objects.filter(**data).first()
        if not user:
            user = User.objects.create_superuser(
                password=settings.IMB_USER_SECRETS['pass'],
                **data
            )
        return user


EXTERNAL_USERS = ExternalUsers()
