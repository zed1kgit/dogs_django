from django.conf import settings
from django.core.mail import send_mail


def send_register_email(email):
    send_mail(
        subject='Поздравляем с регистрацией',
        message='Вы успешно зарегистрировались!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )

def send_new_password(email, new_password):
    send_mail(
        subject='Вы успешно изменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
