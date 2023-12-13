# routers.py

class ExternalDBRouter:
    """
    A router to control all database operations on models in the external database.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read external_db models go to external_db.
        """
        if model._meta.app_label == 'texeclientapp':
            return 'texeclient'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write external_db models go to external_db.
        """
        if model._meta.app_label == 'texeclientapp':
            return 'texeclient'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the external_app is involved.
        """
        if obj1._meta.app_label == 'texeclientapp' or obj2._meta.app_label == 'texeclientapp':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the external_app only appears in the 'external_db' database.
        """
        if app_label == 'texeclientapp':
            return db == 'texeclient'
        return None
