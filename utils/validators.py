import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class PhoneValidator:
    message = 'Phone number must be entered in the format: {}'
    code = 'phone_number'

    def __init__(self, len_digits: int = 12):
        self.pattern = fr'^\d{{{len_digits}}}$'
        self.example = '9' * len_digits

    def __call__(self, value):
        if not re.match(self.pattern, value):
            raise ValidationError(
                self.message.format(self.example),
                code=self.code,
                params={'value': value}
            )


@deconstructible
class VehicleNumberValidator:
    message = 'Car number must be entered in the format: 75 A 777 AA'
    code = 'vehicle_number'

    def __call__(self, value: str):
        cleaned = self.clean(value)
        if not all(x.isdigit() or x.isupper() for x in cleaned):
            raise ValidationError(message=self.message, code=self.code)

    @classmethod
    def clean(cls, value) -> list:
        return re.split(r'\s+', value)
