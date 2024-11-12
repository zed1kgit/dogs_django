from django.db.models.signals import post_save
from django.dispatch import receiver

from dogs.models import Dog
from dogs.services import send_congratulation_mail_task


@receiver(post_save, sender=Dog)
def congratulation_mail(sender, instance, **kwargs):
    if instance.view_count % 100 == 0 and instance.owner:
        send_congratulation_mail_task.delay(instance.owner.email, instance.id, instance.view_count)