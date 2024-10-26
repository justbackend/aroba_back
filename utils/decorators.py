from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required


def permission_required_multiple(perm: str, methods: tuple):
    def decorator(cls):
        for method in methods:
            if hasattr(cls, method):
                decorated_method = (
                    method_decorator(permission_required(perm, raise_exception=True))
                    (getattr(cls, method))
                )
                setattr(cls, method, decorated_method)
        return cls

    return decorator
