from django.core.cache import cache
from . import models


def get_user_perms(user_id: int) -> list:
    perms = cache.get(f'apis_perm_{user_id}')
    if perms is None:
        apis = models.APIRoute.objects.filter(actions__users__id=user_id).distinct()
        data = list(
            map(lambda api: dict(dynamic=api.dynamic, name=api.name, method=api.method, route=api.route), apis)
        )
        cache.set(f'apis_perm_{user_id}', data)

    return perms
