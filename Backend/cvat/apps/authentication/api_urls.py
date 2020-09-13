from django.urls import path
from django.conf import settings
from rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView)
from rest_auth.registration.views import RegisterView
from .views import SigningView
from rest_framework.response import Response
from rest_framework import status


# 继承 RegisterView
class CVATRegisterView(RegisterView):
    # 重写 create 方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(self.get_response_data(user),
                            status=status.HTTP_201_CREATED,
                            headers=headers)
        # 验证失败时，返回错误信息
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_200_OK)


# 继承 LoginView
class CVATLoginView(LoginView):
    # 重写 post 方法
    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data, context={'request': request})
        if self.serializer.is_valid():
            self.login()
            return self.get_response()
        else:
            print(self.serializer.errors)
            return Response(self.serializer.errors, status=status.HTTP_200_OK)


urlpatterns = [
    path('login', CVATLoginView.as_view(), name='rest_login'),
    path('logout', LogoutView.as_view(), name='rest_logout'),
    path('signing', SigningView.as_view(), name='signing')
]

if settings.DJANGO_AUTH_TYPE == 'BASIC':
    urlpatterns += [
        path('register', CVATRegisterView.as_view(), name='rest_register'),
        path('password/reset', PasswordResetView.as_view(),
             name='rest_password_reset'),
        path('password/reset/confirm', PasswordResetConfirmView.as_view(),
             name='rest_password_reset_confirm'),
        path('password/change', PasswordChangeView.as_view(),
             name='rest_password_change'),
    ]
