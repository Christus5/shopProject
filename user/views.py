from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, HttpResponse, redirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import View

from user.forms import *


class LoginView(View):
    template_name = 'user/user_login.html'

    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, {
            'login_form': AuthenticationForm()
        })

    def post(self, request, *args, **kwargs) -> 'HttpResponse':
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        login_form = AuthenticationForm(request=request, data=request.POST)

        if login_form.is_valid():
            login(request, login_form.get_user())
            return redirect(settings.LOGIN_REDIRECT_URL)

        return render(request, self.template_name, {
            'login_form': login_form
        })


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)


class RegisterView(View):
    template_name = 'user/user_registration.html'

    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        registration_form = RegistrationForm()
        return render(request, self.template_name, {
            'registration_form': registration_form
        })

    def post(self, request, *args, **kwargs) -> 'HttpResponse':
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        registration_form = RegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()
            messages.success(request, f"""Successfully registered {registration_form.cleaned_data['username']}""")
            return redirect(settings.LOGOUT_REDIRECT_URL)

        return render(request, self.template_name, {
            'registration_form': registration_form
        })
