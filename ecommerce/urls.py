from django.urls import path

from ecommerce.views import *

app_name = 'ecommerce'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('item/details/<pk>/', ItemView.as_view(), name='item'),
    path('item/create/', ItemCreateView.as_view(), name='create_item'),
    path('item/create/info/', ItemCreateInfoView.as_view(), name='create_item_info'),
    path('item/create/image/', ImageCreationView.as_view(), name='create_item_image'),
    path('item/create/details/<pk>', ItemDetailsView.as_view(), name='item_create_details'),

    path('order/<pk>/', OrderView.as_view(), name='order'),
    path('order/<pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),

    path('cart/<int:cart_id>/', CartDetailsView.as_view(), name='cart'),
    path('cart/<int:cart_id>/checkout', CartCheckoutView.as_view(), name='cart_checkout'),

    path('store/', StoreView.as_view(), name='store'),
    path('profile/', ProfileView.as_view(), name='profile')
]
