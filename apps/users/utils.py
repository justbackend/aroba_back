from apps.users.models import APIRoute


def get_user_perms(request, route: str, path: str) -> list:
    user_id = request.user.id
    first_part = path.split('/')[0]
    apis = APIRoute.objects.filter(
        actions__roles__users__id=user_id,
        route=route,
        method=request.method,
        name__startswith=first_part
    ).distinct()
    return list(map(lambda x: x.cleaned_data, apis))

