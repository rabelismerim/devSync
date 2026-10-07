from django.urls import path

from .views import login, login_msal_redirect


urlpatterns = [
    path('login/', login, name='login'),
    path('login_msal_redirect/<path:redirect_uri>/', login_msal_redirect, name='login_msal_redirect')
]
