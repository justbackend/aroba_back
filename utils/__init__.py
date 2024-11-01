__all__ = (
    'APIException',
    'PageNumberPagination',
    'PhoneValidator',
    'VehicleNumberValidator',
    'permission_required_cls',
    'now',
    'UserNameSerializer',
    'IsActive',
    "RolePermission",
    'get_object',
    'send_me',
)

from datetime import datetime
from zoneinfo import ZoneInfo
from django.conf import settings

from .exceptions import APIException
from .paginations import PageNumberPagination
from .validators import PhoneValidator, VehicleNumberValidator
from .decorators import permission_required_cls
from .utility import get_object, send_me
from utils.customs.permissions import IsActive, RolePermission

from .serializers import (
    UserNameSerializer,
    PointNameSerializer,
    PointLonLatSerializer,
    ClientNameSerializer,
)


def now(timezone: str = settings.TIME_ZONE):
    return datetime.now(ZoneInfo(timezone))
