from django.urls import path
from .views import *


urlpatterns = [
    path('register/', register_view, name='register-page'),
    path('login/', login_view, name='login-page'),
    path('logout/', logout_view, name='logout-page'),

    # activation du compte
    path('activate/<uidb64>/<token>/', activate_view, name='activate-page'),

    # dashboard
    path('dashboard/', dashboard_view, name='dashboard-page'),
    path('', dashboard_view, name='dashboard-page'),

    # password
    path('forget-password/', forgetPassword_view, name='forget-pwd-page'),
    path('reset-pwd-validate/<uidb64>/<token>/', reset_pwd_validate_view, name='reset-pwd-validate-page'),
    path('reset-password/', resetPassword_view, name='reset-pwd-page'),
]

