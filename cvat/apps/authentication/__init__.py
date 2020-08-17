from enum import Enum


default_app_config = 'cvat.apps.authentication.apps.AuthenticationConfig'


class AUTH_ROLE(Enum):
    ADMIN = 'admin'
    USER = 'user'
    ANNOTATOR = 'annotator'
    OBSERVER = 'observer'

    def __str__(self):
        return self.value
