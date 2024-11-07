from django.core.management import BaseCommand

from config.celery import app as celery_app

class Command(BaseCommand):

    def handle(self, *args, **options):
        argv = [
            'worker',
            '--loglevel=info',
            '--pool=solo'
        ]
        celery_app.worker_main(argv)
