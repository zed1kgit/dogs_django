from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        admin = User.objects.create(
            email='admin@gmail.com',
            first_name='Admin',
            last_name='Adminov',
            role='admin',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        admin.set_password('qwerty')
        admin.save()
        print('Admin created')

        moderator = User.objects.create(
            email='moderator@gmail.com',
            first_name='Moderator',
            last_name='Moderov',
            role='moderator',
            is_staff=True,
            is_superuser=False,
            is_active=True
        )

        moderator.set_password('qwerty')
        moderator.save()
        print('Moderator created')

        user = User.objects.create(
            email='user@gmail.com',
            first_name='User',
            last_name='Userov',
            role='user',
            is_staff=False,
            is_superuser=False,
            is_active=True
        )

        user.set_password('qwerty')
        user.save()
        print('User created')
