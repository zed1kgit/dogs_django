from django.conf import settings
from django.db import models

from users.models import NULLABLE


class Category(models.Model):
    """
    Модель категории (например, порода собак). Включает название и описание.

    Атрибуты:
        name (CharField): Название категории.
        description (CharField): Описание категории.

    Методы:
        __str__ (str): Возвращает название категории.

    Метакласс:
        verbose_name (str): Название модели в единственном числе.
        verbose_name_plural (str): Название модели во множественном числе.
    """
    name = models.CharField(max_length=100, verbose_name='breed')
    description = models.CharField(max_length=1000, verbose_name='description')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'breed'
        verbose_name_plural = 'breeds'


class Dog(models.Model):
    """
    Модель собаки. Включает имя, категорию, фото, дату рождения, активность, количество просмотров и владельца.

    Атрибуты:
        name (CharField): Имя собаки.
        category (ForeignKey): Категория (например, порода собак).
        photo (ImageField): Фотография собаки.
        birth_date (DateField): Дата рождения собаки.
        is_active (BooleanField): Активен ли питомец.
        view_count (PositiveIntegerField): Количество просмотров.
        owner (ForeignKey): Владелец собаки.

    Методы:
        __str__ (str): Возвращает имя собаки вместе с категорией.

    Метакласс:
        verbose_name (str): Название модели в единственном числе.
        verbose_name_plural (str): Название модели во множественном числе.
    """
    name = models.CharField(max_length=250, verbose_name='dog_name')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='breed')
    photo = models.ImageField(upload_to='dogs/', verbose_name='image', **NULLABLE)
    birth_date = models.DateField(verbose_name='birth_date', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='active')
    view_count = models.PositiveIntegerField(default=0, verbose_name='view_count')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='owner', **NULLABLE)

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        verbose_name = 'dog'
        verbose_name_plural = 'dogs'

class Parent(models.Model):
    """
    Родительская модель. Связана с моделью собаки. Включает имя, категорию, дату рождения и ссылку на собаку.

    Атрибуты:
        name (Charify): Имя родителя.
        category (ForeignKey): Категория (например, порода собак).
        birth_date (DateField): Дата рождения родителя.
        dog (ForeignKey): Собака, связанная с родителем.

    Методы:
        __str__ (str): Возвращает имя родителя вместе с категорией.

    Метакласс:
        verbose_name (str): Название модели в единственном числе.
        verbose_name_plural (str): Название модели во множественном числе.
    """
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, verbose_name='dog_name')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='breed')
    birth_date = models.DateField(verbose_name='birth_date', **NULLABLE)

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        verbose_name = 'parent'
        verbose_name_plural = 'parents'
