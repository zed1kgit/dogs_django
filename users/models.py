from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class UserRoles(models.TextChoices):
    """
    Класс для выбора ролей пользователя.
    """
    ADMIN = 'admin', _('admin')
    MODERATOR = 'moderator', _('moderator')
    USER = 'user', _('user')


class User(AbstractUser):
    """
    Модель пользователя, расширяющая стандартную модель Django.

    Поля:
        username (None): Поле отключено.
        email (EmailField): Уникальный адрес электронной почты.
        role (CharField): Роль пользователя, выбирается из вариантов UserRoles.
        first_name (CharField): Имя пользователя.
        last_name (CharField): Фамилия пользователя.
        phone (CharField): Номер телефона (необязательное поле).
        telegram (CharField): Никнейм в Telegram (необязательное поле).
        avatar (ImageField): Аватар пользователя (необязательное поле).
        is_active (BooleanField): Признак активности пользователя.

    Методы:
        __str__(): Строковое представление объекта пользователя.

    Метакласс:
        verbose_name: Название модели в единственном числе.
        verbose_name_plural: Название модели во множественном числе.
        ordering: Сортировка по полю id.
    """

    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.USER)
    first_name = models.CharField(max_length=150, verbose_name='First name', default='Anonymous')
    last_name = models.CharField(max_length=150, verbose_name='Last name', default='Anonymous')
    phone = models.CharField(max_length=35, verbose_name='telephone_number', **NULLABLE)
    telegram = models.CharField(max_length=150, verbose_name='Telegram_username', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Avatar', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Active')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Возвращает строку, представляющую объект пользователя.
        """
        return f'{self.email}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['id']
