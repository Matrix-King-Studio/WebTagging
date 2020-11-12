from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'cvat.apps.authentication'

    def ready(self):
        from .auth import register_signals

        register_signals()
