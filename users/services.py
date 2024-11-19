from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task


def send_register_email(email):
    """
    Отправка письма с поздравлением о регистрации.

    Аргументы:
        email (str): Адрес электронной почты получателя.
    """
    send_mail(
        subject='Поздравляем с регистрацией',
        message='Вы успешно зарегистрировались!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )


def send_new_password(email, new_password):
    """
    Отправка письма с новым паролем.

    Аргументы:
        email (str): Адрес электронной почты получателя.
        new_password (str): Новый пароль пользователя.
    """
    send_mail(
        subject='Вы успешно изменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )


@shared_task
def send_register_email_task(email):
    """
    Задание Celery для асинхронной отправки письма с поздравлением о регистрации.

    Аргументы:
        email (str): Адрес электронной почты получателя.
    """
    return send_register_email(email)
