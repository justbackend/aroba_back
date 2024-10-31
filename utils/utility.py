from django.http import Http404


def get_object(model, *args, **kwargs):
    obj = model.objects.filter(*args, **kwargs).first()
    if not obj:
        raise Http404
    return obj
