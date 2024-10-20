from tabnanny import verbose

from django.db import models

from users.models import NULLABLE

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='breed')
    description = models.CharField(max_length=1000, verbose_name='description')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'breed'
        verbose_name_plural = 'breeds'


class Dog(models.Model):
    name = models.CharField(max_length=250, verbose_name='dog_name')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='breed')
    photo = models.ImageField(upload_to='dogs/', verbose_name='image', **NULLABLE)
    birth_date = models.DateField(verbose_name='birth_date', **NULLABLE)

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        verbose_name = 'dog'
        verbose_name_plural = 'dogs'
