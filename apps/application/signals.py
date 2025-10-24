# apps/manufacturers/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Manufacturer
from .tasks import send_status_change_message_task



@receiver(post_save, sender=Manufacturer)
def manufacturer_created(sender, instance, created, **kwargs):
    
    if created:
        send_status_change_message_task.delay(instance.id, instance.status, is_created=True)


@receiver(pre_save, sender=Manufacturer)
def manufacturer_status_changed(sender, instance, **kwargs):

    if not instance.pk:
        return 
    
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    
    if old_instance.status != instance.status:
        send_status_change_message_task.delay(instance.id, instance.status)