class DefaultDatabaseRouter:
    """
    A database router to ensure that all database operations for apps other than 'imb'
    are directed to the 'default' database.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read data for apps other than 'imb' go to the 'default' database.
        """
        if model._meta.app_label != 'imb':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write data for apps other than 'imb' go to the 'default' database.
        """
        if model._meta.app_label != 'imb':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both models are in the 'default' database or both in the same database
        other than 'imb'.
        """
        if obj1._state.db == 'default' and obj2._state.db == 'default':
            return True
        if obj1._meta.app_label != 'imb' and obj2._meta.app_label != 'imb':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Allow migrations on the 'imb' database for the 'imb' app,
        and on the 'default' database for apps other than 'imb'.
        """
        if app_label == 'imb':
            if model_name == 'contact':
                return db == 'default'
            return False
        return db == 'default'
