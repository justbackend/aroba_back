from django.db import models


class Manager(models.Manager):
    def get_queryset(self):
        return super(Manager, self).get_queryset().order_by('-id')
