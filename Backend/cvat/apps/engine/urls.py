from django.urls import path, include

from rest_framework import routers

from . import views
from ..restrictions.views import RestrictionsViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('projects', views.ProjectViewSet)
router.register('tasks', views.TaskViewSet)
router.register('jobs', views.JobViewSet)
router.register('logs', views.LogViewSet)
router.register('users', views.UserViewSet)
router.register('server', views.ServerViewSet, basename='server')
router.register('reviews', views.ReviewViewSet)
router.register('issues', views.IssueViewSet)
router.register('comments', views.CommentViewSet)
router.register('restrictions', RestrictionsViewSet, basename='restrictions')

urlpatterns = [
    path('api/v1/auth/', include('cvat.apps.authentication.api_urls')),
    path('api/v1/', include((router.urls, 'cvat'), namespace='v1'))
]
