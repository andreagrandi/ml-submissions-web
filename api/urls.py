from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path(r'users/', views.UserCreate.as_view(), name='account-create'),
    path(r'login/', obtain_auth_token, name='api-login'),
]
