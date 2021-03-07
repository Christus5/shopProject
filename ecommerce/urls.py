from django.urls import path

from ecommerce.views import *

app_name = 'ecommerce'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('item/<int:pk>/', ItemAPIView.as_view(), name='item'),
    path('item/create/', ItemCreateAPIView.as_view(), name='create_item'),


    path('order/<pk>/', OrderAPIView.as_view(), name='order'),

    path('store/', StoreAPIView.as_view(), name='store'),
]
