from django.urls import path
from .views import *


urlpatterns = [
    path('register/', register_view, name='register-page'),
    path('login/', login_view, name='login-page'),
    path('logout/', logout_view, name='logout-page'),

    # activation du compte
    path('activate/<uidb64>/<token>/', activate_view, name='activate-page'),

    path('dashboard/', dashboard_view, name='dashboard-page'),
    path('', dashboard_view, name='dashboard-page'),
]

