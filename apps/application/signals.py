from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from asgiref.sync import sync_to_async
from apps.application.models import (
    TenderResponse, Order, Payment, Manufacturer, Tender
)
from apps.application.services.notification_service import notification_service
import asyncio
import logging

logger = logging.getLogger(__name__)

def run_async_notification(func, *args, **kwargs):
    """Async notification funksiyasini Django da ishlatish"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(func(*args, **kwargs))
        loop.close()
    except Exception as e:
        logger.error(f"Error running async notification: {e}")

@receiver(post_save, sender=TenderResponse)
def tender_response_notification(sender, instance, created, **kwargs):
    """Yangi tender javobi yaratilganda notification yuborish"""
    if created:
        run_async_notification(
            notification_service.send_tender_response_notification,
            instance
        )

@receiver(post_save, sender=Order)
def order_update_notification(sender, instance, **kwargs):
    """Buyurtma holati o'zgarishida notification yuborish"""
    if instance.pk:  # Yangi yaratilgan emas, yangilangan
        run_async_notification(
            notification_service.send_order_update_notification,
            instance,
            instance.status
        )

@receiver(post_save, sender=Payment)
def payment_success_notification(sender, instance, **kwargs):
    """To'lov muvaffaqiyatli bo'lganda notification yuborish"""
    if (instance.status == 'completed' and 
        instance.completed_at and 
        not hasattr(instance, '_notification_sent')):
        
        # Notification yuborilganini belgilash
        instance._notification_sent = True
        
        run_async_notification(
            notification_service.send_payment_success_notification,
            instance
        )

@receiver(post_save, sender=Manufacturer)
def manufacturer_subscription_notification(sender, instance, **kwargs):
    """Zavod obuna muddati tugashiga eslatma yuborish"""
    if (instance.subscription_expires and 
        instance.status == 'verified' and
        instance.is_active):
        
        days_left = (instance.subscription_expires - timezone.now()).days
        
        # 30, 7, 1 kun qolganda eslatma
        if days_left in [30, 7, 1]:
            run_async_notification(
                notification_service.send_subscription_expires_notification,
                instance
            )

@receiver(post_save, sender=Tender)
def new_tender_notification(sender, instance, created, **kwargs):
    """Yangi tender yaratilganda zavodlarga xabar yuborish"""
    if created and instance.status == 'active':
        run_async_notification(
            notification_service.send_new_tender_notification,
            instance
        )

# Signal larni ro'yxatdan o'tkazish
def register_signals():
    """Barcha signal larni ro'yxatdan o'tkazish"""
    # Bu funksiya apps.py da chaqiriladi
    pass
