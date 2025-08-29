import asyncio
from typing import List, Optional, Dict, Any
from django.conf import settings
from django.utils import timezone
from apps.application.models import BotUser, Notification, Tender, TenderResponse, Order, Payment, Manufacturer
from apps.bot.misc import get_dispatcher_and_bot
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """Bot orqali foydalanuvchilarga xabarlar yuborish uchun service"""
    
    def __init__(self):
        self.bot = None
        self.dp = None
    
    async def _get_bot(self):
        """Bot instance ni olish"""
        if self.bot is None:
            self.dp, self.bot = get_dispatcher_and_bot()
        return self.bot
    
    async def send_notification(self, user: BotUser, title: str, message: str, 
                               notification_type: str = "system", data: Optional[Dict] = None):
        """Foydalanuvchiga notification yuborish"""
        try:
            # Ma'lumotlar bazasida notification yaratish
            notification = Notification.objects.create(
                user=user,
                notification_type=notification_type,
                title=title,
                message=message,
                data=data
            )
            
            # Bot orqali xabar yuborish
            bot = await self._get_bot()
            
            # Telegram ID mavjudligini tekshirish
            if user.telegram_id:
                try:
                    await bot.send_message(
                        chat_id=user.telegram_id,
                        text=f"🔔 <b>{title}</b>\n\n{message}",
                        parse_mode="HTML"
                    )
                    logger.info(f"Notification sent to user {user.telegram_id}: {title}")
                except Exception as e:
                    logger.error(f"Failed to send notification to user {user.telegram_id}: {e}")
            else:
                logger.warning(f"User {user.id} has no telegram_id")
                
            return notification
            
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            return None
    
    async def send_tender_response_notification(self, tender_response: TenderResponse):
        """Tender javobi haqida mijozga xabar yuborish"""
        try:
            customer = tender_response.tender.customer
            manufacturer = tender_response.manufacturer
            
            title = "🆕 Yangi tender javobi"
            message = (
                f"<b>{manufacturer.company_name}</b> zavodi sizning "
                f"<b>#{tender_response.tender.lot_number}</b> tenderingizga javob berdi.\n\n"
                f"💬 Xabar: {tender_response.message[:100]}...\n"
                f"⏰ Vaqt: {tender_response.created_at.strftime('%d.%m.%Y %H:%M')}"
            )
            
            await self.send_notification(
                user=customer.user,
                title=title,
                message=message,
                notification_type="tender_response",
                data={
                    "tender_id": tender_response.tender.id,
                    "response_id": tender_response.id,
                    "manufacturer_id": manufacturer.id
                }
            )
            
        except Exception as e:
            logger.error(f"Error sending tender response notification: {e}")
    
    async def send_order_update_notification(self, order: Order, status: str):
        """Buyurtma holati o'zgarishida xabar yuborish"""
        try:
            status_messages = {
                "confirmed": "✅ Buyurtmangiz tasdiqlandi",
                "in_production": "🏭 Buyurtmangiz ishlab chiqarishda",
                "ready": "📦 Buyurtmangiz tayyor",
                "shipped": "🚚 Buyurtmangiz yuborildi",
                "delivered": "🎉 Buyurtmangiz yetkazildi"
            }
            
            title = "📋 Buyurtma yangilanishi"
            message = (
                f"{status_messages.get(status, 'Buyurtma holati o\'zgartirildi')}\n\n"
                f"📋 Buyurtma: #{order.order_number}\n"
                f"🏭 Zavod: {order.manufacturer.company_name}\n"
                f"💰 Summa: ${order.total_amount}\n"
                f"📅 Yetkazib berish: {order.delivery_date.strftime('%d.%m.%Y')}"
            )
            
            await self.send_notification(
                user=order.customer.user,
                title=title,
                message=message,
                notification_type="order_update",
                data={
                    "order_id": order.id,
                    "status": status
                }
            )
            
        except Exception as e:
            logger.error(f"Error sending order update notification: {e}")
    
    async def send_payment_success_notification(self, payment: Payment):
        """To'lov muvaffaqiyatli bo'lganda xabar yuborish"""
        try:
            payment_type_names = {
                "subscription": "Obuna",
                "catalog_access": "Katalog kirish",
                "video_meeting": "Video uchrashuv",
                "factory_tour": "Zavod sayohati",
                "verification": "Tekshirish",
                "personal_manager": "Shaxsiy menejer",
                "training": "O'qitish"
            }
            
            title = "💳 To'lov muvaffaqiyatli"
            message = (
                f"✅ <b>{payment_type_names.get(payment.payment_type, 'Xizmat')}</b> "
                f"uchun to'lov muvaffaqiyatli amalga oshirildi!\n\n"
                f"💰 Summa: {payment.amount} {payment.currency}\n"
                f"💳 Usul: {payment.get_payment_method_display()}\n"
                f"🕐 Vaqt: {payment.completed_at.strftime('%d.%m.%Y %H:%M')}"
            )
            
            await self.send_notification(
                user=payment.user,
                title=title,
                message=message,
                notification_type="payment_success",
                data={
                    "payment_id": payment.id,
                    "amount": str(payment.amount),
                    "currency": payment.currency
                }
            )
            
        except Exception as e:
            logger.error(f"Error sending payment success notification: {e}")
    
    async def send_subscription_expires_notification(self, manufacturer: Manufacturer):
        """Obuna muddati tugashiga eslatma yuborish"""
        try:
            days_left = (manufacturer.subscription_expires - timezone.now()).days
            
            if days_left <= 30:  # 30 kundan kam qolganda
                title = "⚠️ Obuna muddati tugaydi"
                message = (
                    f"🔔 <b>{manufacturer.company_name}</b> zavodi!\n\n"
                    f"📅 Sizning obunangiz {days_left} kundan keyin tugaydi.\n"
                    f"💳 Obunani yangilash uchun to'lov qiling va "
                    f"katalogda faol bo'lib qoling.\n\n"
                    f"💰 Narx: $200 (6 oy)"
                )
                
                await self.send_notification(
                    user=manufacturer.user,
                    title=title,
                    message=message,
                    notification_type="subscription_expires",
                    data={
                        "manufacturer_id": manufacturer.id,
                        "days_left": days_left
                    }
                )
                
        except Exception as e:
            logger.error(f"Error sending subscription expires notification: {e}")
    
    async def send_new_tender_notification(self, tender: Tender):
        """Yangi tender haqida zavodlarga xabar yuborish"""
        try:
            # Faqat obuna bo'lgan va tasdiqlangan zavodlarga xabar yuborish
            manufacturers = Manufacturer.objects.filter(
                status="verified",
                subscription_expires__gt=timezone.now(),
                is_active=True
            )
            
            title = "🆕 Yangi tender"
            message = (
                f"📋 <b>Yangi tender #{tender.lot_number}</b>\n\n"
                f"🏭 Mijoz: {tender.customer.company_name}\n"
                f"📦 Mahsulot: {tender.get_product_segment_display()}\n"
                f"🔢 Hajm: {tender.order_quantity}\n"
                f"📅 Muddat: {tender.delivery_date.strftime('%d.%m.%Y')}\n\n"
                f"💬 Tender haqida batafsil ma'lumot olish uchun javob bering!"
            )
            
            # Barcha tegishli zavodlarga xabar yuborish
            for manufacturer in manufacturers:
                if manufacturer.product_segment == tender.product_segment:
                    await self.send_notification(
                        user=manufacturer.user,
                        title=title,
                        message=message,
                        notification_type="tender_response",
                        data={
                            "tender_id": tender.id,
                            "lot_number": tender.lot_number
                        }
                    )
                    
        except Exception as e:
            logger.error(f"Error sending new tender notification: {e}")
    
    async def send_system_notification(self, users: List[BotUser], title: str, message: str):
        """Tizim xabarini bir nechta foydalanuvchilarga yuborish"""
        try:
            for user in users:
                await self.send_notification(
                    user=user,
                    title=title,
                    message=message,
                    notification_type="system"
                )
                
        except Exception as e:
            logger.error(f"Error sending system notification: {e}")
    
    async def send_tour_package_notification(self, customer: 'Customer', tour_package: 'TourPackage'):
        """Zavod safari paketi haqida mijozga xabar yuborish"""
        try:
            title = "🏭 Zavod safari paketi"
            message = (
                f"🎯 <b>{tour_package.name}</b> paketi tanlandi!\n\n"
                f"📅 Davomiyligi: {tour_package.duration_days} kun\n"
                f"💰 Narxi: ${tour_package.price_usd} / {tour_package.price_som} so'm\n"
                f"👥 Maksimal: {tour_package.max_participants} kishi\n"
                f"🏭 Zavodlar: {tour_package.max_manufacturers} ta\n\n"
                f"📋 {tour_package.description[:200]}..."
            )
            
            await self.send_notification(
                user=customer.user,
                title=title,
                message=message,
                notification_type="system",
                data={
                    "tour_package_id": tour_package.id,
                    "package_type": tour_package.package_type
                }
            )
            
        except Exception as e:
            logger.error(f"Error sending tour package notification: {e}")
    
    def get_user_notifications(self, user: BotUser, limit: int = 20) -> List[Notification]:
        """Foydalanuvchining notificationlarini olish"""
        return Notification.objects.filter(user=user).order_by('-created_at')[:limit]
    
    def mark_notification_as_read(self, notification_id: int) -> bool:
        """Notificationni o'qilgan deb belgilash"""
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            return True
        except Notification.DoesNotExist:
            return False
    
    def mark_all_notifications_as_read(self, user: BotUser) -> int:
        """Foydalanuvchining barcha notificationlarini o'qilgan deb belgilash"""
        count = Notification.objects.filter(user=user, is_read=False).update(is_read=True)
        return count


# Global instance
notification_service = NotificationService()
