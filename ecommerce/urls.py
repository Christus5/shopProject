from django.urls import path

from ecommerce.views import *

app_name = 'ecommerce'
urlpatterns = [
    path('', HomeView.as_view(), name='home')
]
