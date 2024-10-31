import re
from django.core.exceptions import ValidationError


def validate_password(field):
    pattern = re.compile('^[a-zA-Z0-9]+$')
    if not pattern.match(field):
        raise ValidationError('Пароль должен содержать A-Z, a-z буквы и 0-9 цифры')
    if not 6 <= len(field) <= 12:
        raise ValidationError('Длинна пароля должна быть от 6 до 12 символов')
