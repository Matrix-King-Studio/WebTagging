from django.urls import path
from . import views


urlpatterns = [
    path('api/v1/detection/<int:taskId>/<int:number>', views.detection, name="detection"),
]
