from django.contrib import admin
from django.urls import path, include
from django.apps import apps

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cvat.apps.engine.urls')),
    path('django-rq/', include('django_rq.urls')),
    path('auth/', include('cvat.apps.authentication.urls')),
    path('documentation/', include('cvat.apps.documentation.urls')),
]

if apps.is_installed('cvat.apps.tf_annotation'):
    urlpatterns.append(path('tensorflow/annotation/', include('cvat.apps.tf_annotation.urls')))

if apps.is_installed('cvat.apps.git'):
    urlpatterns.append(path('git/repository/', include('cvat.apps.git.urls')))

if apps.is_installed('cvat.apps.reid'):
    urlpatterns.append(path('reid/', include('cvat.apps.reid.urls')))

if apps.is_installed('cvat.apps.auto_annotation'):
    urlpatterns.append(path('auto_annotation/', include('cvat.apps.auto_annotation.urls')))

if apps.is_installed('cvat.apps.dextr_segmentation'):
    urlpatterns.append(path('dextr/', include('cvat.apps.dextr_segmentation.urls')))

if apps.is_installed('cvat.apps.log_viewer'):
    urlpatterns.append(path('analytics/', include('cvat.apps.log_viewer.urls')))

if apps.is_installed('silk'):
    urlpatterns.append(path('profiler/', include('silk.urls')))

# new feature by Mohammad
if apps.is_installed('cvat.apps.auto_segmentation'):
    urlpatterns.append(path('tensorflow/segmentation/', include('cvat.apps.auto_segmentation.urls')))
