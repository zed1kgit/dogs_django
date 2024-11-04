from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm

from users.models import User
from users.validators import validate_password


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar',)


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        temp_data = self.cleaned_data
        validate_password(temp_data['password1'])
        if temp_data['password1'] != temp_data['password2']:
            raise forms.ValidationError('password_mismatch')
        return temp_data['password2']


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    pass


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'telegram', 'avatar',)


class UserChangePasswordForm(StyleFormMixin, PasswordChangeForm):
    pass
