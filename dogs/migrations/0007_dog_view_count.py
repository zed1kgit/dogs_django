# Generated by Django 5.0.9 on 2024-11-06 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0006_dog_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='dog',
            name='view_count',
            field=models.PositiveIntegerField(default=0, verbose_name='view_count'),
        ),
    ]
