__all__ = (
    'APIException',
    'PhoneValidator',
    'VehicleNumberValidator',
    'UserNameSerializer',
    'permission_required_cls',
    'now',
    'get_object',
    'send_me',
    'permissions',
)

from datetime import datetime
from zoneinfo import ZoneInfo
from django.conf import settings

from .paginations import PageNumberPagination
from .exceptions import APIException
from .validators import PhoneValidator, VehicleNumberValidator
from .decorators import permission_required_cls
from .utility import get_object, send_me

from .serializers import (
    UserNameSerializer,
    PointNameSerializer,
    PointLonLatSerializer,
    ClientNameSerializer,
)


def now(timezone: str = settings.TIME_ZONE):
    return datetime.now(ZoneInfo(timezone))
