import string
import random


from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.shortcuts import reverse, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserChangePasswordForm, UserForm
from users.models import User
from users.services import send_register_email, send_new_password, send_register_email_task


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login_user')
    template_name = 'users/register_user.html'

    def form_valid(self, form):
        self.object = form.save()
        send_register_email_task.delay(self.object.email)
        return super().form_valid(form)


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
    template_name = 'users/logout_user.html'


@login_required
def user_generate_new_password(request):
    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))


class UserListView(ListView):
    model = User
    paginate_by = 3
    extra_context = {
        'title': 'Все пользователи сайта'
    }
    template_name = 'users/users.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset

class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'
