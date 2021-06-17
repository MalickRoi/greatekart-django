from django.urls import path
from .views import *

urlpatterns = [
    path('', store_view, name='store-page'),
    path('<slug:category_slug>/', store_view, name='detail-store-page'),
    path('<slug:category_slug>/<slug:product_slug>/', product_detail_view, name='product-detail-page'),
]

