from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, HttpResponse, redirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import View, FormView, CreateView, RedirectView

from ecommerce.models import Cart
from user.forms import *


class LoginView(FormView):
    template_name = 'user/user_login.html'
    form_class = AuthenticationForm
    success_url = settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = context.get('form')
        return context

    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().get(request)

    def post(self, request, *args, **kwargs) -> 'HttpResponse':
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().post(request)


@method_decorator(login_required, name='dispatch')
class LogoutView(RedirectView):
    permanent = True
    pattern_name = 'user:login'

    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        logout(request)
        return super().get(request)


class RegisterView(CreateView):
    template_name = 'user/user_registration.html'
    form_class = RegistrationForm
    success_url = settings.LOGOUT_REDIRECT_URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registration_form'] = context.get('form')
        return context

    def form_valid(self, form):
        form.save()
        Cart(user=User.objects.get(username=form.save(commit=False))).save()
        messages.success(self.request, f"""Successfully registered {form.cleaned_data['username']}""")
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().get(request)

    def post(self, request, *args, **kwargs) -> 'HttpResponse':
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        return super().post(request)
