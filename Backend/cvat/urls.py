from django.contrib import admin
from django.urls import path, include
from django.apps import apps

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auto/', include("cvat.apps.autoAnnotation.urls")),
    path('', include('cvat.apps.engine.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('auth/', include('cvat.apps.authentication.urls')),
]

if apps.is_installed('cvat.apps.dataset_repo'):
    urlpatterns.append(path('git/repository/', include('cvat.apps.dataset_repo.urls')))

if apps.is_installed('cvat.apps.log_viewer'):
    urlpatterns.append(path('analytics/', include('cvat.apps.log_viewer.urls')))

if apps.is_installed('cvat.apps.lambda_manager'):
    urlpatterns.append(path('', include('cvat.apps.lambda_manager.urls')))

if apps.is_installed('silk'):
    urlpatterns.append(path('profiler/', include('silk.urls')))
