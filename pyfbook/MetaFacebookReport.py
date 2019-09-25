from dbstream import DBStream
from googleauthentication import GoogleAuthentication


class MetaFacebookReport:
    def __init__(self, googleauthentication: GoogleAuthentication, config_path, dbstream: DBStream):
        self.googleauthentication = googleauthentication
        self.config_path = config_path
        self.dbstream = dbstream
