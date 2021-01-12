from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, authenticate
from rest_auth.registration.views import RegisterView
from rest_auth.serializers import PasswordChangeSerializer
from rest_framework import views, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from furl import furl

from . import forms
from . import signature

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_auth.views import PasswordChangeView, sensitive_post_parameters_m, LoginView


def register_user(request):
    if request.method == 'POST':
        form = forms.NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)


@method_decorator(name='post', decorator=swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['url'],
        properties={'url': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    responses={'200': openapi.Response(description='text URL')}
))
class SigningView(views.APIView):
    def post(self, request):
        url = request.data.get('url')
        if not url:
            raise ValidationError('Please provide `url` parameter')

        signer = signature.Signer()
        url = self.request.build_absolute_uri(url)
        sign = signer.sign(self.request.user, url)

        url = furl(url).add({signature.QUERY_PARAM: sign}).url
        return Response(url)


# 继承 RegisterView
class Register(RegisterView):
    # 重写 create 方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(self.get_response_data(user), status=status.HTTP_201_CREATED, headers=headers)
        # 验证失败时，返回错误信息
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_200_OK)


# 继承 LoginView
class Login(LoginView):
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
