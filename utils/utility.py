import requests
from django.core.cache import cache
from django.http import Http404


def get_object(model, *args, **kwargs):
    obj = model.objects.filter(*args, **kwargs).first()
    if not obj:
        raise Http404
    return obj


def send_me(message):
    token = '7061215872:AAE9FzKlpOiP0fekIrvyyoUEvJqdAOQKC6E'
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        'chat_id': 6050173548,
        'text': str(message),
        'parse_mode': 'html',
    }
    requests.post(url, params=data)


def clear_users_perms(users):
    for user in users:
        if type(user) is int:
            cache.delete(f"apis_perm_{user}")
        else:
            cache.delete(f"apis_perm_{user.id}")


def clear_user_profile_data(users):
    for user in users:
        if type(user) is int:
            cache.delete(f"user_profile_{user}")
        else:
            cache.delete(f"user_profile_{user.id}")

