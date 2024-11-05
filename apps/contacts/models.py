from django.db import models
from utils import BaseModel, PhoneValidator


class Contact(BaseModel):
    full_name = models.CharField(max_length=100, verbose_name="Full Name")
    phone = models.CharField(max_length=20, validators=[PhoneValidator()], verbose_name='Phone')
    trailer_front = models.ImageField(
        null=True, blank=True,
        upload_to='contact_images/',
        verbose_name='Trailer front',
    )
    trailer_back = models.ImageField(
        null=True, blank=True,
        upload_to='contact_images/',
        verbose_name='Trailer back',
    )
    license_front = models.ImageField(
        null=True, blank=True,
        upload_to='contact_images/',
        verbose_name='License front',
    )
    license_back = models.ImageField(
        null=True, blank=True,
        upload_to='contact_images/',
        verbose_name='License back',
    )
    track_front = models.ImageField(
        null=True, blank=True,
        upload_to='contact_images/',
        verbose_name='Track front',
    )
    track_back = models.ImageField(
        null=True, blank=True,
        upload_to='contact_images/',
        verbose_name='Track back',
    )

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        db_table = 'contacts'

    def __str__(self):
        return self.full_name
