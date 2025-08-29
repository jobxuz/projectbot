from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from apps.application.models import BotUser, Notification, Manufacturer
from apps.application.services.notification_service import notification_service
import asyncio
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_notification_task(user_id: int, title: str, message: str, 
                          notification_type: str = "system", data: dict = None):
    """Notification yuborish uchun Celery task"""
    try:
        user = BotUser.objects.get(id=user_id)
        
        # Async notification yuborish
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(
            notification_service.send_notification(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type,
                data=data
            )
        )
        
        loop.close()
        
        if result:
            logger.info(f"Notification sent successfully to user {user_id}")
            return {"success": True, "notification_id": result.id}
        else:
            logger.error(f"Failed to send notification to user {user_id}")
            return {"success": False, "error": "Failed to create notification"}
            
    except BotUser.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return {"success": False, "error": "User not found"}
    except Exception as e:
        logger.error(f"Error sending notification to user {user_id}: {e}")
        return {"success": False, "error": str(e)}

@shared_task
def send_bulk_notifications_task(user_ids: list, title: str, message: str, 
                                notification_type: str = "system", data: dict = None):
    """Ko'p foydalanuvchilarga notification yuborish"""
    success_count = 0
    error_count = 0
    
    for user_id in user_ids:
        try:
            result = send_notification_task.delay(user_id, title, message, notification_type, data)
            if result.get().get("success"):
                success_count += 1
            else:
                error_count += 1
        except Exception as e:
            logger.error(f"Error in bulk notification for user {user_id}: {e}")
            error_count += 1
    
    logger.info(f"Bulk notification completed: {success_count} success, {error_count} errors")
    return {"success_count": success_count, "error_count": error_count}

@shared_task
def notify_manufacturer_created(manufacturer_id: int):
    """Yangi manufacturer yaratilganda notification yuborish"""
    try:
        manufacturer = Manufacturer.objects.get(id=manufacturer_id)
        
        # Admin foydalanuvchilarga xabar
        admin_users = BotUser.objects.filter(type='manufacturer', is_active=True)
        
        for admin_user in admin_users:
            send_notification_task.delay(
                user_id=admin_user.id,
                title="🏭 Yangi zavod qo'shildi",
                message=(
                    f"🔔 <b>{manufacturer.company_name}</b> zavodi ro'yxatdan o'tdi!\n\n"
                    f"👤 F.I.SH: {manufacturer.full_name}\n"
                    f"📍 Manzil: {manufacturer.production_address}\n"
                    f"📱 Telefon: {manufacturer.phone or 'Ko\'rsatilmagan'}\n\n"
                    f"✅ Zavodni tekshirish va tasdiqlash kerak."
                ),
                notification_type="system",
                data={
                    "manufacturer_id": manufacturer.id,
                    "action": "review_required"
                }
            )
        
        logger.info(f"Manufacturer creation notification sent for {manufacturer.company_name}")
        return {"success": True, "notifications_sent": admin_users.count()}
        
    except Manufacturer.DoesNotExist:
        logger.error(f"Manufacturer {manufacturer_id} not found")
        return {"success": False, "error": "Manufacturer not found"}
    except Exception as e:
        logger.error(f"Error sending manufacturer creation notification: {e}")
        return {"success": False, "error": str(e)}

@shared_task
def check_subscription_expiry():
    """Obuna muddati tugash eslatmalarini yuborish"""
    now = timezone.now()
    
    # 30 kun, 7 kun, 1 kun qolganda eslatma
    for days in [30, 7, 1]:
        target_date = now + timedelta(days=days)
        
        manufacturers = Manufacturer.objects.filter(
            status='verified',
            subscription_expires__date=target_date.date(),
            user__is_active=True
        )
        
        for manufacturer in manufacturers:
            send_notification_task.delay(
                user_id=manufacturer.user.id,
                title="⚠️ Obuna muddati tugaydi",
                message=(
                    f"🔔 <b>{manufacturer.company_name}</b> zavodi!\n\n"
                    f"📅 Sizning obunangiz {days} kundan keyin tugaydi.\n"
                    f"💳 Obunani yangilash uchun to'lov qiling va "
                    f"katalogda faol bo'lib qoling.\n\n"
                    f"💰 Narx: $200 (6 oy)"
                ),
                notification_type="subscription_expires",
                data={
                    "manufacturer_id": manufacturer.id,
                    "days_left": days
                }
            )
    
    logger.info(f"Subscription expiry check completed at {now}")
    return {"message": "Subscription expiry notifications sent"}

@shared_task
def cleanup_old_notifications():
    """Eski notificationlarni tozalash"""
    old_date = timezone.now() - timedelta(days=30)
    
    deleted_count = Notification.objects.filter(
        created_at__lt=old_date,
        is_read=True  # Faqat o'qilgan notificationlarni o'chirish
    ).delete()[0]
    
    logger.info(f"Cleaned up {deleted_count} old notifications")
    return {"deleted_count": deleted_count}

@shared_task
def send_daily_summary():
    """Kunlik hisobot yuborish"""
    today = timezone.now().date()
    
    # Bugungi notificationlar statistikasi
    today_notifications = Notification.objects.filter(created_at__date=today)
    
    stats = {
        "total": today_notifications.count(),
        "by_type": {}
    }
    
    for notification_type, display_name in Notification.NotificationTypeChoices.choices:
        count = today_notifications.filter(notification_type=notification_type).count()
        if count > 0:
            stats["by_type"][display_name] = count
    
    # Admin foydalanuvchilarga hisobot yuborish
    admin_users = BotUser.objects.filter(type="customer", is_active=True)[:5]  # Birinchi 5 admin
    
    summary_message = (
        f"📊 <b>Bugungi notification hisoboti</b>\n\n"
        f"📅 Sana: {today.strftime('%d.%m.%Y')}\n"
        f"📈 Jami yuborilgan: {stats['total']}\n\n"
    )
    
    if stats["by_type"]:
        summary_message += "<b>Turlari bo'yicha:</b>\n"
        for type_name, count in stats["by_type"].items():
            summary_message += f"• {type_name}: {count}\n"
    
    for admin_user in admin_users:
        send_notification_task.delay(
            user_id=admin_user.id,
            title="📊 Kunlik notification hisoboti",
            message=summary_message,
            notification_type="system",
            data={"daily_summary": True, "date": today.isoformat(), "stats": stats}
        )
    
    logger.info(f"Daily summary sent: {stats}")
    return stats

@shared_task
def process_tender_notifications(tender_id: int):
    """Yangi tender haqida zavodlarga xabar yuborish"""
    try:
        from apps.application.models import Tender
        
        tender = Tender.objects.get(id=tender_id)
        
        # Async notification yuborish
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        loop.run_until_complete(
            notification_service.send_new_tender_notification(tender)
        )
        
        loop.close()
        
        logger.info(f"Tender notifications sent for tender {tender_id}")
        return {"success": True, "tender_id": tender_id}
        
    except Exception as e:
        logger.error(f"Error sending tender notifications for tender {tender_id}: {e}")
        return {"success": False, "error": str(e)}

@shared_task
def process_order_status_notification(order_id: int, status: str):
    """Buyurtma holati o'zgarishi haqida xabar yuborish"""
    try:
        from apps.application.models import Order
        
        order = Order.objects.get(id=order_id)
        
        # Async notification yuborish
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        loop.run_until_complete(
            notification_service.send_order_update_notification(order, status)
        )
        
        loop.close()
        
        logger.info(f"Order status notification sent for order {order_id}")
        return {"success": True, "order_id": order_id, "status": status}
        
    except Exception as e:
        logger.error(f"Error sending order status notification for order {order_id}: {e}")
        return {"success": False, "error": str(e)}

@shared_task
def check_notification_health():
    """Notification tizimini tekshirish"""
    try:
        # Bot holati tekshiruvi
        bot = notification_service._get_bot()
        
        # Test notification yaratish
        test_user = BotUser.objects.filter(is_active=True).first()
        if test_user:
            # Faqat database ga yozish, bot orqali yubormaslik
            test_notification = Notification.objects.create(
                user=test_user,
                notification_type="system",
                title="🔧 System Health Check",
                message="Notification tizimi health check",
                data={"health_check": True, "timestamp": timezone.now().isoformat()}
            )
            
            logger.info("Notification health check completed successfully")
            return {"success": True, "test_notification_id": test_notification.id}
        else:
            logger.warning("No active users found for health check")
            return {"success": False, "error": "No active users"}
            
    except Exception as e:
        logger.error(f"Notification health check failed: {e}")
        return {"success": False, "error": str(e)}

@shared_task 
def daily_user_stats():
    """Kunlik foydalanuvchilar statistikasi"""
    try:
        today = timezone.now().date()
        
        # Foydalanuvchilar statistikasi
        total_users = BotUser.objects.count()
        active_users = BotUser.objects.filter(is_active=True).count()
        customers = BotUser.objects.filter(type="customer").count()
        manufacturers = BotUser.objects.filter(type="manufacturer").count()
        
        # Bugungi yangi foydalanuvchilar
        new_users_today = BotUser.objects.filter(created_at__date=today).count()
        
        # Zavodlar statistikasi
        verified_manufacturers = Manufacturer.objects.filter(status="verified").count()
        active_subscriptions = Manufacturer.objects.filter(
            subscription_expires__gt=timezone.now()
        ).count()
        
        # Bugungi faollik
        today_notifications = Notification.objects.filter(created_at__date=today).count()
        
        stats = {
            "date": today.isoformat(),
            "total_users": total_users,
            "active_users": active_users,
            "customers": customers,
            "manufacturers": manufacturers,
            "new_users_today": new_users_today,
            "verified_manufacturers": verified_manufacturers,
            "active_subscriptions": active_subscriptions,
            "today_notifications": today_notifications
        }
        
        logger.info(f"Daily user stats: {stats}")
        return stats
        
    except Exception as e:
        logger.error(f"Error generating daily user stats: {e}")
        return {"success": False, "error": str(e)}

@shared_task
def process_tour_package_notification(tour_package_id: int, customer_id: int):
    """Zavod safari paketi haqida xabar yuborish"""
    try:
        from apps.application.models import TourPackage, Customer
        
        tour_package = TourPackage.objects.get(id=tour_package_id)
        customer = Customer.objects.get(id=customer_id)
        
        # Async notification yuborish
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        loop.run_until_complete(
            notification_service.send_tour_package_notification(customer, tour_package)
        )
        
        loop.close()
        
        logger.info(f"Tour package notification sent for package {tour_package_id}")
        return {"success": True, "tour_package_id": tour_package_id, "customer_id": customer_id}
        
    except Exception as e:
        logger.error(f"Error sending tour package notification for package {tour_package_id}: {e}")
        return {"success": False, "error": str(e)}

@shared_task
def create_default_tour_packages():
    """Standart zavod safari paketlarini yaratish"""
    try:
        from apps.application.models import TourPackage, TourPackageFeature, TourPackagePrice
        
        # Standart paket
        standard_package, created = TourPackage.objects.get_or_create(
            package_type="standard",
            defaults={
                "name": "Standart Zavod Safari",
                "description": "O'zbekistondagi eng yaxshi to'qimachilik zavodlariga 2 kunlik sayohat. Tashish, gid va zavod tashriflari kiritilgan.",
                "duration_days": 2,
                "price_usd": 150,
                "price_usd": 150,
                "price_som": 1800000,
                "includes_transport": True,
                "includes_accommodation": False,
                "includes_guide": True,
                "max_manufacturers": 3,
                "max_participants": 5,
                "is_active": True,
                "is_featured": True,
                "order": 1
            }
        )
        
        if created:
            # Paket xususiyatlari
            features = [
                {"name": "Tashish", "description": "Zavodlar o'rtasida tashish", "icon": "🚗", "order": 1},
                {"name": "Professional gid", "description": "Tajribali gid bilan", "icon": "👨‍💼", "order": 2},
                {"name": "Zavod tashriflari", "description": "3 ta zavodga tashrif", "icon": "🏭", "order": 3},
                {"name": "Lunch", "description": "Tushlik taomlari", "icon": "🍽️", "order": 4},
            ]
            
            for feature_data in features:
                TourPackageFeature.objects.create(
                    tour_package=standard_package,
                    **feature_data
                )
            
            # Narxlar (ishtirokchilar soniga qarab)
            prices = [
                {"participants_count": 1, "price_usd": 200, "price_som": 2400000},
                {"participants_count": 2, "price_usd": 150, "price_som": 1800000},
                {"participants_count": 3, "price_usd": 120, "price_som": 1440000},
                {"participants_count": 4, "price_usd": 100, "price_som": 1200000},
                {"participants_count": 5, "price_usd": 90, "price_som": 1080000},
            ]
            
            for price_data in prices:
                TourPackagePrice.objects.create(
                    tour_package=business_package,
                    **price_data
                )
        
        # Biznes paket
        business_package, created = TourPackage.objects.get_or_create(
            package_type="business",
            defaults={
                "name": "Biznes Zavod Safari",
                "description": "Premium zavod safari. 3 kunlik sayohat, turar joy, tarjimon va madaniy dastur bilan.",
                "duration_days": 3,
                "price_usd": 300,
                "price_som": 3600000,
                "includes_transport": True,
                "includes_accommodation": True,
                "includes_guide": True,
                "includes_translator": True,
                "includes_cultural_program": True,
                "max_manufacturers": 5,
                "max_participants": 3,
                "is_active": True,
                "is_featured": True,
                "order": 2
            }
        )
        
        if created:
            # Paket xususiyatlari
            features = [
                {"name": "Premium tashish", "description": "Qulay avtomobil", "icon": "🚙", "order": 1},
                {"name": "4 yulduzli mehmonxona", "description": "Toshkent markazida", "icon": "🏨", "order": 2},
                {"name": "Professional tarjimon", "description": "Rus/Ingliz tillari", "icon": "🗣️", "order": 3},
                {"name": "5 ta zavod", "description": "Eng yaxshi zavodlar", "icon": "🏭", "order": 4},
                {"name": "Madaniy dastur", "description": "Toshkent ekskursiyasi", "icon": "🎭", "order": 5},
            ]
            
            for feature_data in features:
                TourPackageFeature.objects.create(
                    tour_package=business_package,
                    **feature_data
                )
            
            # Narxlar
            prices = [
                {"participants_count": 1, "price_usd": 400, "price_som": 4800000},
                {"participants_count": 2, "price_usd": 300, "price_som": 3600000},
                {"participants_count": 3, "price_usd": 250, "price_som": 3000000},
            ]
            
            for price_data in prices:
                TourPackagePrice.objects.create(
                    tour_package=business_package,
                    **price_data
                )
        
        logger.info("Default tour packages created successfully")
        return {"success": True, "packages_created": 2}
        
    except Exception as e:
        logger.error(f"Error creating default tour packages: {e}")
        return {"success": False, "error": str(e)}
