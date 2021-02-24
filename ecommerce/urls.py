from django.urls import path

from ecommerce.views import *

app_name = 'ecommerce'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('item/<pk>/', ItemView.as_view(), name='item'),
    path('order/<pk>/', OrderView.as_view(), name='order'),
    path('order/<pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('cart/<int:cart_id>/', CartDetailsView.as_view(), name='cart'),
    path('store/', StoreView.as_view(), name='store')
]
