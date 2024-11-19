import string
import random

def slug_generator(size=20, chars=string.ascii_letters + string.digits):
    """
    Генерирует уникальный слаг (случайная строка символов).

    Аргументы:
        size (int): Длина генерируемого слога. По умолчанию 20.
        chars (str): Символы, используемые для генерации слага. По умолчанию включает буквы латинского алфавита и цифры.

    Возвращает:
        str: Сгенерированный слаг заданной длины.
    """
    return ''.join(random.choice(chars) for _ in range(size))