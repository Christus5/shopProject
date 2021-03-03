from django.urls import path
from django.views.generic import TemplateView

from rest_framework.authtoken.views import *

from user.views import *

app_name = 'user'
urlpatterns = [
    path('', TemplateView.as_view(
        template_name='user/user_login.html'
    ), name='login'),
    path('authenticate/', obtain_auth_token, name='authenticate'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_api_view, name='register')
]
