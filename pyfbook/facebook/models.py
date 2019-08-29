import os

from pyfbook.facebook.tools.execute_query import execute_query


class SystemUser:
    def __init__(self, id, app_id_name, app_secret_name, access_token_name):
        self.id = id
        self.app_id_name = app_id_name
        self.app_id = os.environ[app_id_name]
        self.app_secret_name = app_secret_name
        self.app_secret = os.environ[app_secret_name]
        self.access_token_name = access_token_name
        self.access_token = os.environ[access_token_name]

    @staticmethod
    def all(config):
        schema_name = config.get('schema_name')
        r = execute_query('SELECT * FROM %s.app_system_user' % schema_name, config)
        return [SystemUser(**result) for result in r]

    @staticmethod
    def get(config, id):
        schema_name = config.get('schema_name')
        r = execute_query('SELECT * FROM %s.app_system_user WHERE id=%s' % (schema_name, id), config)
        if not r:
            print('SystemUser does not exist')
            exit(1)
        return SystemUser(**r[0])
