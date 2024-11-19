from dataclasses import dataclass
from functools import cached_property
from .models import User


@dataclass(slots=True)
class ExternalUsers:

    @cached_property
    def imb_user(self):
        data = dict(username='imb', first_name='IMB', last_name='IMB', is_superuser=True)
        user = User.objects.filter(**data).first()
        if not user:
            user = User.objects.create_user(password='imb_2024', **data)
        return user

