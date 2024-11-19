from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

from users.models import User
from users.validators import validate_password


class StyleFormMixin:
    """
    Миксин для добавления стиля к полям форм.
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация миксина. Добавляет класс 'form-control' ко всем полям формы.

        Аргументы:
            args: Позиционные аргументы.
            kwargs: Именованные аргументы.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для редактирования профиля пользователя.

    Метаданные:
        model (User): Модель пользователя.
        fields (tuple): Поля, доступные для редактирования.
    """

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar',)


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма для регистрации нового пользователя.

    Метаданные:
        model (User): Модель пользователя.
        fields (tuple): Поля, доступные для заполнения при регистрации.

    Метод:
        clean_password2(self): Проверка совпадения введенных паролей и их валидность.
    """

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        """
        Проверка совпадения введенных паролей и их валидность.

        Возвращает:
            str: Повторенный пароль, если он совпадает с первым и проходит валидацию.

        Исключения:
            ValidationError: Если пароли не совпадают или не проходят валидацию.
        """
        temp_data = self.cleaned_data
        validate_password(temp_data['password1'])
        if temp_data['password1'] != temp_data['password2']:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return temp_data['password2']


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """
    Форма для аутентификации пользователя.
    """
    pass


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для обновления информации о пользователе.

    Метаданные:
        model (User): Модель пользователя.
        fields (tuple): Поля, доступные для редактирования.
    """

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'avatar',)


class UserChangePasswordForm(StyleFormMixin, PasswordChangeForm):
    """
    Форма для изменения пароля пользователя.

    Метод:
        clean_new_password2(self): Проверка совпадения новых паролей и их валидность.
    """

    def clean_new_password2(self):
        """
        Проверка совпадения новых паролей и их валидность.

        Возвращает:
            str: Новый пароль, если он совпадает с повторенным и проходит валидацию.

        Исключения:
            ValidationError: Если новые пароли не совпадают или не проходят валидацию.
        """
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        validate_password(password1)
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        password_validation.validate_password(password2, self.user)
        return password2