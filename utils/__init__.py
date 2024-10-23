__all__ = (
    'APIException',
)

from rest_framework.exceptions import APIException as DRFAPIException


class APIException(DRFAPIException):
    status_code = 400
    default_detail = {'response': 'Something went wrong'}