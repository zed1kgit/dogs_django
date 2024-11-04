from datetime import datetime

from django import forms

from dogs.models import Dog


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class DogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        exclude = ('owner',)

    def clean_birth_date(self):
        if self.cleaned_data['birth_date']:
            cd = self.cleaned_data['birth_date']
            now_year = datetime.now().year
            if now_year - cd.year > 100:
                raise forms.ValidationError('Собака должна быть моложе 100 лет')
            return cd
        return
