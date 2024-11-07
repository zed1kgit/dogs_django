from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from celery import shared_task
from django.shortcuts import get_object_or_404

from dogs.models import Category, Dog


def get_categories_cache():
    if settings.CACHE_ENABLED:
        key = 'category_list'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        category_list = Category.objects.all()

    return category_list


def send_congratulation_mail(email, obj, count):
    send_mail(
        subject=f'Поздравляем {count} просмотров!!',
        message=f'Ваша собака - {obj.name}, преодолела {count} просмотров!!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )


@shared_task
def send_congratulation_mail_task(email, obj_id, count):
    obj = get_object_or_404(Dog, id=obj_id)
    return send_congratulation_mail(email, obj, count)
