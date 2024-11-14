from django.db import models
from django.conf import settings
from django.urls import reverse
from users.models import NULLABLE
from dogs.models import Dog


class Review(models.Model):
    title = models.CharField(max_length=150, verbose_name='title')
    slug = models.SlugField(max_length=25, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(verbose_name='content')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='timestamp')
    sign_of_review = models.BooleanField(default=True, verbose_name='sign of')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='author')
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, verbose_name='dog')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('reviews:detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
