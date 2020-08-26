from django.urls import path
from . import views

urlpatterns = [
    path('<path:path>', views.LogViewerProxy.as_view())
]
