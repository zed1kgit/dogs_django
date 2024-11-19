from django import forms

from dogs.models import Dog
from reviews.models import Review
from dogs.forms import StyleFormMixin


class ReviewForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для создания и редактирования отзывов.

    Поля:
        dog (ModelChoiceField): Скрытое поле для выбора собаки, к которой относится отзыв.
        title (CharField): Заголовок отзыва.
        content (TextInput): Содержимое отзыва.
        slug (SlugField): Скрытое поле для уникального идентификатора отзыва.

    Метаданные:
        model (Review): Модель отзыва.
        fields (list): Список полей, включаемых в форму.
    """

    dog = forms.ModelChoiceField(queryset=Dog.objects.all(), required=False, widget=forms.HiddenInput())
    title = forms.CharField(max_length=150, label='Заголовок')
    content = forms.TextInput()
    slug = forms.SlugField(max_length=20, initial='temp_slug', widget=forms.HiddenInput())

    class Meta:
        model = Review
        fields = ['dog', 'title', 'content', 'slug']
