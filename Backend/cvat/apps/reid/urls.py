from django.urls import path
from . import views

urlpatterns = [
    path('start/job/<int:jid>', views.start),
    path('cancel/<int:jid>', views.cancel),
    path('check/<int:jid>', views.check),
    path('enabled', views.enabled),
]
