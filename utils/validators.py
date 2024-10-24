import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class PhoneValidator:
    message = 'Phone number must be entered in the format: {}'
    code = 'phone_number'

    def __init__(self, pattern: str = r'^\d{12}$', example: str = '999999999999'):
        self.pattern = pattern
        self.example = example

    def __call__(self, value):
        if self.compare(value):
            raise ValidationError(
                self.message.format(self.example),
                code=self.code,
                params={'value': value}
            )

    def compare(self, value):
        return not re.match(self.pattern, value)

    def clean(self, value):
        return value
