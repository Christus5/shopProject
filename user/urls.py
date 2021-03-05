from django.urls import path, include
from rest_framework.authtoken.views import *

from user.views import *

app_name = 'user'
urlpatterns = [
    path('authenticate/', obtain_auth_token, name='authenticate'),
    path('register/', register_api_view, name='register')
]
