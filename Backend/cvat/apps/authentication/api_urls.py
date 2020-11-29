from django.urls import path
from django.conf import settings
from .views import SigningView, PasswordChange, Login, Register
from rest_auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView


urlpatterns = [
    path('login', Login.as_view(), name='rest_login'),
    path('logout', LogoutView.as_view(), name='rest_logout'),
    path('signing', SigningView.as_view(), name='signing')
]

if settings.DJANGO_AUTH_TYPE == 'BASIC':
    urlpatterns += [
        path('register', Register.as_view(), name='rest_register'),
        path('password/reset', PasswordResetView.as_view(), name='rest_password_reset'),
        path('password/reset/confirm', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
        path('password/change', PasswordChange.as_view(), name='rest_password_change'),
    ]
