from datetime import datetime

from django import forms

from dogs.models import Dog, Parent


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


class DogForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для создания и редактирования информации о собаках.

    Атрибуты:
        model (Dog): Модель собак.
        exclude (tuple): Поля, исключаемые из формы.

    Методы:
        clean_birth_date(self): Валидация даты рождения собаки.
    """
    class Meta:
        model = Dog
        exclude = ('owner', 'is_active', 'view_count')

    def clean_birth_date(self):
        """
        Валидация даты рождения собаки.

        Аргументы:
            self: Экземпляр формы.

        Поднимает исключение:
            ValidationError: Если собака старше 100 лет.

        Возвращает:
            cleaned_data['birth_date']: Дата рождения собаки.
        """
        if self.cleaned_data['birth_date']:
            cd = self.cleaned_data['birth_date']
            now_year = datetime.now().year
            if now_year - cd.year > 100:
                raise forms.ValidationError('Собака должна быть моложе 100 лет')
            return cd
        return


class DogAdminForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для создания и редактирования информации о собаках в админке.

    Атрибуты:
        model (Dog): Модель собак.
        fields (list): Все поля модели доступны для редактирования.

    Методы:
        clean_birth_date(self): Валидация даты рождения собаки.
    """
    class Meta:
        model = Dog
        fields = '__all__'

    def clean_birth_date(self):
        """
        Валидация даты рождения собаки.

        Аргументы:
            self: Экземпляр формы.

        Поднимает исключение:
            ValidationError: Если собака старше 100 лет.

        Возвращает:
            cleaned_data['birth_date']: Дата рождения собаки.
        """
        if self.cleaned_data['birth_date']:
            cd = self.cleaned_data['birth_date']
            now_year = datetime.now().year
            if now_year - cd.year > 100:
                raise forms.ValidationError('Собака должна быть моложе 100 лет')
            return cd
        return


class ParentForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для редактирования родительской модели.

    Атрибуты:
        model (Parent): Модель родителя.
        fields (list): Все поля модели доступны для редактирования.
    """
    class Meta:
        model = Parent
        fields = '__all__'
