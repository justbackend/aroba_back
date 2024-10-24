import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.core.validators import RegexValidator


@deconstructible
class PhoneValidator:
    message = 'Phone number must be entered in the format: {}'
    code = 'phone_number'

    def __init__(self, pattern: str = r'^\d{12}$', example: str = '999999999999'):
        self.pattern = pattern
        self.example = example

    def __call__(self, value):
        if not re.match(self.pattern, value):
            raise ValidationError(
                self.message.format(self.example),
                code=self.code,
                params={'value': value}
            )

