from django.apps import AppConfig


class AutoAnnotationConfig(AppConfig):
    name = "cvat.apps.auto_annotation"

    def ready(self):
        from .permissions import setup_permissions

        setup_permissions()
