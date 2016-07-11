from django.apps import AppConfig
from django.db import connection
from django.db.models.signals import pre_migrate


def create_extension_callback(sender, **kwargs):
    '''
    Always create PostgreSQL LTREE extension if it doesn't already exist
    on the database before syncing the database.
    Requires PostgreSQL 9.1 or newer.
    TODO: still requires that the user is a postgres superuser.
    http://stackoverflow.com/questions/20723100/why-can-only-a-superuser-create-extension-hstore-but-not-on-heroku
    '''
    cursor = connection.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS ltree")


class SaplingConfig(AppConfig):
    name = 'lsapling'

    def ready(self):
        pre_migrate.connect(create_extension_callback, sender=self)
