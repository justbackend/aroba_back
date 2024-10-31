from django.http import Http404


def get_object(model, **kwargs):
    obj = model.objects.filter(**kwargs).first()
    if not obj:
        raise Http404
    return obj
