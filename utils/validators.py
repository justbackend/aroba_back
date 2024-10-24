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
        if not self.compare(cleaned):
            raise ValidationError(message=self.message, code=self.code)

    @classmethod
    def clean(cls, value) -> list:
        return re.split(r'\s+', value)

    @classmethod
    def compare(cls, cleaned):
        digit = False
        upper = False

        checking = []
        for char in cleaned:
            isdigit = char.isdigit()
            isupper = char.isupper()
            digit = digit or isdigit
            upper = upper or isupper

            checking.append(isupper or isdigit)
        return digit and upper and all(checking)

