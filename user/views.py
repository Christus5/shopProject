from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, HttpResponse, redirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import View, FormView, CreateView, RedirectView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ecommerce.models import Cart
from user.forms import *


# class LoginView(FormView):
#     template_name = 'user/user_login.html'
#     form_class = AuthenticationForm
#     success_url = settings.LOGIN_REDIRECT_URL
#
#     def form_valid(self, form):
#         login(self.request, form.get_user())
#         return redirect(self.success_url)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['login_form'] = context.get('form')
#         return context
#
#     def get(self, request, *args, **kwargs) -> 'HttpResponse':
#         if request.user.is_authenticated:
#             return redirect(settings.LOGIN_REDIRECT_URL)
#
#         return super().get(request)
#
#     def post(self, request, *args, **kwargs) -> 'HttpResponse':
#         if request.user.is_authenticated:
#             return redirect(settings.LOGIN_REDIRECT_URL)
#
#         return super().post(request)
from user.serializers import UserRegisterSerializer


@method_decorator(login_required, name='dispatch')
class LogoutView(RedirectView):
    permanent = True
    pattern_name = 'user:login'

    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        logout(request)
        return super().get(request)


@api_view(['POST'])
def register_api_view(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "User created successfully!"
            data['username'] = user.username
            data['email'] = user.email
            data['token'] = Token.objects.get(user=user).key
        else:
            data = serializer.errors
        return Response(data)