from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, HttpResponse, redirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import RedirectView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        token = Token.objects.create(user=user)
        data['token'] = token.key
        return Response(data)
