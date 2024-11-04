from django.core.cache import cache
from . import models


def get_apis_perm(user) -> list:
    perms = cache.get(f'apis_perm_{user.id}')
    if perms is None:
        apis = models.APIRoute.objects.filter(actions__users_id=user).distinct()
        data = list(
            map(lambda api: dict(dynamic=api.dynamic, name=api.name, method=api.method, route=api.route), apis)
        )
        cache.set(f'apis_perm_{user.id}', data)

    return perms
