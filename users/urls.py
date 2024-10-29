from django.urls import path

from users.apps import UsersConfig
from users.views import user_register_view, user_login_view

app_name = UsersConfig.name

urlpatterns = [
    path('', user_login_view, name='login_user'),
    path('register/', user_register_view, name='register_user'),
]