from django.db import models

from utils.managers import Manager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Manager()

    class Meta:
        abstract = True

