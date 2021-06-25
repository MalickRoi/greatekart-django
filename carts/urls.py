from django.urls import path
from .views import *

urlpatterns = [
    path('', cart_view, name='cart-page'),
    path('add_cart/<int:product_id>/', add_cart_view, name='add-cart-page'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', remove_cart_view, name='remove-cart-page'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', remove_cart_item_view, name='remove-cart-item-page'),
    path('checkout/', checkout_view, name='checkout-page'),
]

