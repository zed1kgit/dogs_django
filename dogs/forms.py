from django import forms

from dogs.models import Dog

class StyleFormMixin:
    def __init__(self,*args , **kwargs):
        super().__init__(*args , **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class DogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Dog
        fields = '__all__'