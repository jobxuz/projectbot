# apps/manufacturers/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Manufacturer
from .tasks import send_status_change_message_task



@receiver(pre_save, sender=Manufacturer)
def manufacturer_status_changed(sender, instance, **kwargs):
    print("ishga tushdi")

    if not instance.pk:
        return  
    
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    
    if old_instance.status != instance.status:
        print(instance.status)
        send_status_change_message_task.delay(instance.id, instance.status)