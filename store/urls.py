from django.urls import path
from .views import *

urlpatterns = [
    path('', store_view, name='store-page'),
    path('category/<slug:category_slug>/', store_view, name='detail-store-page'),
    path('category/<slug:category_slug>/<slug:product_slug>/', product_detail_view, name='product-detail-page'),
    path('search/', search_view, name='search-page'),
]

