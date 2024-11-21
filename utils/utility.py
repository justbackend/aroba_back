from typing import Type

import requests
from django.core.cache import cache
from django.db.models import Q, Model
from django.http import Http404
from dataclasses import dataclass, field

from utils import BaseModel


def get_object(
        model,
        filters: dict = None,
        select_related: list = None,
        prefetch_related: list = None,
        q_objects: Q = None,
        *args,
        **kwargs,
):
    """
    Retrieve a single object from the database with optional filters,
    select_related, and prefetch_related optimizations.

    Args:
        model: Django model class to query.
        filters (dict): Additional keyword filters to apply.
        select_related (list): Related fields for SQL JOIN optimization.
        prefetch_related (list): Related fields for queryset prefetching.
        q_objects: Positional arguments for filtering (e.g., Q objects).
        **kwargs: Additional keyword arguments for filtering.

    Returns:
        obj: The retrieved object, or raises Http404 if not found.
    """
    filters = filters or {}
    select_related = select_related or []
    prefetch_related = prefetch_related or []
    q_objects = q_objects or Q()

    filters.update(**kwargs)

    # Apply filters and relations
    queryset = (
        model.objects
        .prefetch_related(*prefetch_related)
        .select_related(*select_related)
        .filter(q_objects, *args, **filters)  # Merge filters and kwargs
    )

    obj = queryset.first()
    if not obj:
        raise Http404
    return obj


def send_me(message):
    token = '7362304291:AAHsSLbhZozUvZboGh_brEXMFp22bMkwF4E'
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        'chat_id': 1172189473,
        'text': str(message),
        'parse_mode': 'html',
    }
    requests.post(url, params=data)


def clear_users_perms(users):
    for user in users:
        if type(user) is int:
            cache.delete(f"apis_perm_{user}")
            cache.delete(f"has_perms_{user}")
        else:
            cache.delete(f"apis_perm_{user.id}")
            cache.delete(f"has_perms_{user.id}")


def clear_user_profile_data(users):
    for user in users:
        if type(user) is int:
            cache.delete(f"user_profile_{user}")
        else:
            cache.delete(f"user_profile_{user.id}")


@dataclass
class MainCheckout:
    model: Type[Model]
    balance_field: str = 'balance'

    @property
    def __checkout(self):
        # Get the first object, or return None if no objects exist
        return self.model.objects.first()

    @property
    def balance(self):
        checkout = self.__checkout
        if checkout:
            return getattr(checkout, self.balance_field)
        raise ValueError("No checkout instance found.")

    def add(self, amount):
        checkout = self.__checkout
        if checkout:
            current_balance = getattr(checkout, self.balance_field)
            setattr(checkout, self.balance_field, current_balance + amount)
            checkout.save()
        else:
            raise ValueError("No checkout instance found. Cannot add balance.")