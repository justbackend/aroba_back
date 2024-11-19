import requests
from django.core.cache import cache
from django.http import Http404


def get_object(model, filters=None, select_related=None, prefetch_related=None, *args, **kwargs):
    filters = filters or {}
    select_related = select_related or []
    prefetch_related = prefetch_related or []

    obj = (
        model.objects
        .prefetch_related(*prefetch_related)
        .select_related(*select_related)
        .filter(*args, **kwargs, **filters).first()
    )
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

