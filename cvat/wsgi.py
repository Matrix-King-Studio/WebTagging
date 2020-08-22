import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cvat.settings.{}" \
    .format(os.environ.get("DJANGO_CONFIGURATION", "development")))

application = get_wsgi_application()
