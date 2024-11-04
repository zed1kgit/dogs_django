import string
import random

from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserChangePasswordForm, UserForm
from users.models import User
from users.services import send_register_email, send_new_password


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login_user')
    template_name = 'users/register_user.html'


class UserLoginView(LoginView):
    template_name = 'users/login_user.html'
    form_class = UserLoginForm


class UserProfileView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/user_profile.html'

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('users:profile_user')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserChangePasswordForm
    success_url = reverse_lazy('users:profile_user')
    template_name = 'users/user_change_password.html'


class UserLogoutView(LogoutView):
    pass
    # template_name = 'users/logout.html'


def user_logout_view(request):
    logout(request)
    return redirect('dogs:index')


@login_required
def user_generate_new_password(request):
    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))
