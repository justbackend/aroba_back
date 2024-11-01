from django.http import Http404
import requests


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
