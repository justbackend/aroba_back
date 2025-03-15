from django.db import models


class IMBDatabaseManager(models.Manager):
    """
    Custom manager to ensure all operations use the 'imb' database.
    """

    use_in_migrations = False

    def get_queryset(self):
        """
        Override the default queryset to use 'imb' database.
        """
        return super().get_queryset().using('imb')

    def create(self, **kwargs):
        """
        Override the create method to use 'imb' database.
        """
        return super().using('imb').create(**kwargs)

    def bulk_create(self, objs, **kwargs):
        """
        Override the bulk_create method to use 'imb' database.
        """
        return super().using('imb').bulk_create(objs, **kwargs)

    def get(self, *args, **kwargs):
        """
        Override the get method to use 'imb' database.
        """
        return super().using('imb').get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        """
        Override the filter method to use 'imb' database.
        """
        return super().using('imb').filter(*args, **kwargs)

    def update_or_create(self, defaults=None, **kwargs):
        """
        Override update_or_create to use 'imb' database.
        """
        return super().using('imb').update_or_create(defaults=defaults, **kwargs)
