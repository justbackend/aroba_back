from django.db import models


class ActivePointManager(models.Manager):
    def get_queryset(self):
        return super(ActivePointManager, self).get_queryset().filter(deleted=False)
