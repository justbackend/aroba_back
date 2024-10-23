from enum import IntEnum


class OrderStatus(IntEnum):
    DELETED = 0
    NEW = 1
    IN_PROGRESS = 2
    STARTED = 3
    AT_FACTORY = 4
    DISPATCHED = 5
    LOCATION_ASSIGNED = 6
    FINISHED = 7
    REJECTED = 8


API_ROUTE_CHOICES = (
    ('/api/v1/users/', 'Users'),
    ('/api/v1/common/', 'Common'),
)

API_DYNAMIC_CHOICES = (
    ('1', 'Yes'),
    ('0', 'No'),
)

