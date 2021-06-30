from django.urls import path
from .views import *


urlpatterns = [
    path('place-order/', placeOrder_view, name='place-order-page'),
    path('payments/', payments_view, name='payments-page'),
    path('order-complete', order_complete_view, name='order-complete-page'),
]

