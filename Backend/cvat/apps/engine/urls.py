
# Copyright (C) 2018-2019 Intel Corporation
#
# SPDX-License-Identifier: MIT

from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from cvat.apps.restrictions.views import RestrictionsViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="CVAT REST API",
      default_version='v1',
      description="REST API for Computer Vision Annotation Tool (CVAT)",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="nikita.manovich@intel.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.IsAuthenticated,),
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('projects', views.ProjectViewSet)
router.register('tasks', views.TaskViewSet)
router.register('jobs', views.JobViewSet)
router.register('users', views.UserViewSet)
router.register('server', views.ServerViewSet, basename='server')
router.register('plugins', views.PluginViewSet)
router.register('restrictions', RestrictionsViewSet, basename='restrictions')

urlpatterns = [
    # Entry point for a client
    path('', views.dispatch_request),
    path('dashboard/', views.dispatch_request),

    # documentation for API
    path('api/swagger<str:scheme>', views.wrap_swagger(
       schema_view.without_ui(cache_timeout=0)), name='schema-json'),
    path('api/swagger/', views.wrap_swagger(
       schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path('api/docs/', views.wrap_swagger(
       schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),

    # entry point for API
    path('api/v1/auth/', include('cvat.apps.authentication.api_urls')),
    path('api/v1/', include((router.urls, 'cvat'), namespace='v1'))
]
