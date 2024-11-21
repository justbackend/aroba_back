

class DefaultDatabaseRouter:
    """
    A database router to ensure that migrations are applied only on the 'default' database.
    """

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Allow migrations only on the 'default' database.
        """

        return db == 'default' and app_label != 'imb'
