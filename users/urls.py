from django.urls import path

from users.apps import UsersConfig
from users.views import user_logout_view, user_update_view, \
    user_generate_new_password, UserPasswordChangeView, UserRegisterView, UserLoginView, UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(), name='login_user'),
    path('logout/', user_logout_view, name='logout_user'),
    path('register/', UserRegisterView.as_view(), name='register_user'),
    path('profile/', UserProfileView.as_view(), name='profile_user'),
    path('update/', user_update_view, name='update_user'),
    path('profile/generate_password/', user_generate_new_password, name='user_generate_new_password'),
    path('change_password/', UserPasswordChangeView.as_view(), name='change_password_user'),
]
