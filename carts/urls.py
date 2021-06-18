from django.urls import path
from .views import *

urlpatterns = [
    path('', cart_view, name='cart-page'),
    path('add_cart/<int:product_id>/', add_cart_view, name='add-cart-page'),
]

