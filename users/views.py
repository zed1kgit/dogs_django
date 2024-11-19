import string
import random

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.shortcuts import reverse, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserChangePasswordForm, UserForm
from users.models import User
from users.services import send_new_password, send_register_email_task


class UserRegisterView(CreateView):
    """
    Представление для регистрации нового пользователя.

    Атрибуты:
        model (User): Модель пользователя.
        form_class (UserRegisterForm): Форма для регистрации пользователя.
        success_url (reverse_lazy): URL для перенаправления после успешной регистрации.
        template_name (str): Путь к шаблону для отображения формы регистрации.

    Методы:
        form_valid(self, form): Обработчик успешной отправки формы. Сохраняет пользователя и отправляет письмо с подтверждением.
    """

    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login_user')
    template_name = 'users/register_user.html'

    def form_valid(self, form):
        """
        Обработка успешной отправки формы регистрации.

        Аргументы:
            form (UserRegisterForm): Заполненная форма регистрации.

        Возвращает:
            HttpResponseRedirect: Перенаправление на страницу успешного завершения регистрации.
        """
        self.object = form.save()
        send_register_email_task.delay(self.object.email)
        return super().form_valid(form)


class UserLoginView(LoginView):
    """
    Представление для входа пользователя.

    Атрибуты:
        template_name (str): Путь к шаблону для отображения формы входа.
        form_class (UserLoginForm): Форма для авторизации пользователя.
    """
    template_name = 'users/login_user.html'
    form_class = UserLoginForm


class UserProfileView(UpdateView):
    """
    Представление для просмотра профиля пользователя.

    Атрибуты:
        model (User): Модель пользователя.
        form_class (UserForm): Форма для редактирования профиля пользователя.
        template_name (str): Путь к шаблону для отображения профиля.

    Методы:
        get_object(self, queryset=None): Получение текущего пользователя.
    """

    model = User
    form_class = UserForm
    template_name = 'users/user_profile.html'

    def get_object(self, queryset=None):
        """
        Получение текущего пользователя.
        """
        return self.request.user


class UserUpdateView(UpdateView):
    """
    Представление для обновления информации о пользователе.

    Атрибуты:
        model (User): Модель пользователя.
        form_class (UserUpdateForm): Форма для изменения данных пользователя.
        template_name (str): Путь к шаблону для отображения формы изменения данных.
        success_url (reverse_lazy): URL для перенаправления после успешного изменения данных.

    Методы:
        get_object(self, queryset=None): Получение текущего пользователя.
    """

    model = User
    form_class = UserUpdateForm
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('users:profile_user')

    def get_object(self, queryset=None):
        """
        Получение текущего пользователя.

        Аргумент:
            queryset (QuerySet): Набор объектов модели. По умолчанию None.

        Возвращает:
            User: Объект текущего пользователя.
        """
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    """
    Представление для смены пароля пользователя.

    Атрибуты:
        form_class (UserChangePasswordForm): Форма для изменения пароля.
        success_url (reverse_lazy): URL для перенаправления после успешной смены пароля.
        template_name (str): Путь к шаблону для отображения формы смены пароля.
    """

    form_class = UserChangePasswordForm
    success_url = reverse_lazy('users:profile_user')
    template_name = 'users/user_change_password.html'


class UserLogoutView(LogoutView):
    """
    Представление для выхода пользователя из системы.

    Атрибуты:
        template_name (str): Путь к шаблону для отображения страницы выхода.
    """

    template_name = 'users/logout_user.html'


@login_required
def user_generate_new_password(request):
    """
    Функция для генерации нового случайного пароля для пользователя и отправки его на email.
    """
    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))


class UserListView(ListView):
    """
    Представление для списка всех активных пользователей.

    Атрибуты:
        model (User): Модель пользователя.
        paginate_by (int): Количество пользователей на одной странице.
        extra_context (dict): Дополнительный контекст для передачи в шаблон.
        template_name (str): Путь к шаблону для отображения списка пользователей.

    Методы:
        get_queryset(self): Получение набора активных пользователей.
    """

    model = User
    paginate_by = 3
    extra_context = {
        'title': 'Все пользователи сайта'
    }
    template_name = 'users/users.html'

    def get_queryset(self):
        """
        Получение набора активных пользователей.

        Возвращает:
            QuerySet: Набор активных пользователей.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class UserDetailView(DetailView):
    """
    Представление для детального просмотра информации о конкретном пользователе.

    Атрибуты:
        model (User): Модель пользователя.
        template_name (str): Путь к шаблону для отображения детальной информации о пользователе.
    """

    model = User
    template_name = 'users/user_detail.html'
