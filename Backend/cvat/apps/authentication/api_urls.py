from django.urls import path

from rest_auth.views import LogoutView, PasswordChangeView

from .views import SigningView, Login, Register

urlpatterns = [
    path('login', Login.as_view(), name='rest_login'),
    path('signing', SigningView.as_view(), name='signing'),
    path('register', Register.as_view(), name='rest_register'),
    path('logout', LogoutView.as_view(), name='rest_logout'),
    path('password/change', PasswordChangeView.as_view(), name='rest_password_change'),
]
