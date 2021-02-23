from django.urls import path

from ecommerce.views import *

app_name = 'ecommerce'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('item/', ItemView.as_view(), name='item'),
    path('order/<int:order_id>/', OrderDetailsView.as_view(), name='order'),
    path('cart/<int:cart_id>/', CartDetailsView.as_view(), name='cart'),
    path('store/', StoreView.as_view(), name='store')
]
