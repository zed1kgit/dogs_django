from django.db import models
from django.conf import settings
from django.urls import reverse
from users.models import NULLABLE
from dogs.models import Dog


class Review(models.Model):
    """
    Модель отзыва.

    Поля:
        title (CharField): Заголовок отзыва.
        slug (SlugField): Уникальный URL-адрес отзыва.
        content (TextField): Содержимое отзыва.
        timestamp (DateTimeField): Время создания отзыва.
        sign_of_review (BooleanField): Признак наличия подписи под отзывом.
        author (ForeignKey): Автор отзыва.
        dog (ForeignKey): Собака, к которой относится отзыв.

    Методы:
        __str__(): Возвращает заголовок отзыва.
        get_absolute_url(): Возвращает абсолютный URL отзыва.

    Метакласс:
        verbose_name: Название модели в единственном числе.
        verbose_name_plural: Название модели во множественном числе.
    """

    title = models.CharField(max_length=150, verbose_name='title')
    slug = models.SlugField(max_length=25, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(verbose_name='content')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='timestamp')
    sign_of_review = models.BooleanField(default=True, verbose_name='sign of')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='author')
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, verbose_name='dog')

    def __str__(self):
        """
        Возвращает строковое представление объекта отзыва.
        """
        return self.title

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL отзыва.
        """
        return reverse('reviews:detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
