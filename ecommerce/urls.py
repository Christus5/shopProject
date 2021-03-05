from django.urls import path

from ecommerce.views import *

app_name = 'ecommerce'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('item/<int:pk>/', ItemAPIView.as_view(), name='item'),
    path('item/create/', ItemCreateAPIView.as_view(), name='create_item'),


    path('order/<pk>/', OrderAPIView.as_view(), name='order'),

    path('cart/<int:cart_id>/', CartDetailsView.as_view(), name='cart'),
    path('cart/<int:cart_id>/checkout', CartCheckoutView.as_view(), name='cart_checkout'),

    path('store/', StoreAPIView.as_view(), name='store'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('inbox/', InboxView.as_view(), name='inbox')
]
