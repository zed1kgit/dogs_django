import re

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_password(field):
    pattern = re.compile('^[a-zA-Z0-9]+$')
    language = settings.LANGUAGE_CODE
    error_messages = [
        {
            'ru-ru': 'Пароль должен содержать буквы латинского алфавита и цифры!',
            'en-us': 'Password must contain A-Z, a-z, and 0-9 characters!',
        },
        {
            'ru-ru': 'Длина пароля должна быть от 6 до 12 символов!',
            'en-us': 'Password length must be between 6 and 12 characters!',
        }
    ]
    if not pattern.match(field):
        raise ValidationError(
            error_messages[0][language],
            code=error_messages[0][language]
        )
    if not 6 <= len(field) <= 12:
        raise ValidationError(
            error_messages[1][language],
            code=error_messages[1][language]
        )
