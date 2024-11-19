__all__ = (
    'APIException',
    'PhoneValidator',
    'VehicleNumberValidator',
    'UserNameSerializer',
    'RolePermission',
    'IsActive',
    'PayloadPermission',
    'IMBPermission',
    'BaseModel',
    'Manager',
    'now',
    'get_object',
    'send_me',
    'create_serializer',
)

from datetime import datetime
from zoneinfo import ZoneInfo
from django.conf import settings

from .base import BaseModel
from .paginations import PageNumberPagination
from .exceptions import APIException
from .validators import PhoneValidator, VehicleNumberValidator
from .utility import get_object, send_me
from .creators import create_serializer
from .managers import Manager
from .permissions import (
    IsActive,
    RolePermission,
    PayloadPermission,
    IMBPermission
)
from .serializers import (
    UserNameSerializer,
    PointNameSerializer,
    PointLonLatSerializer,
    ClientNameSerializer,
)


def now(timezone: str = settings.TIME_ZONE):
    return datetime.now(ZoneInfo(timezone))
