from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from django.conf import settings
from apps.application.models import BotUser, Notification
import asyncio

notification_router = Router()

@notification_router.message(Command("notifications"))
async def show_notifications(message: Message):
    """Foydalanuvchining notificationlarini ko'rsatish"""
    try:
        # Foydalanuvchini topish
        user = BotUser.objects.filter(telegram_id=message.from_user.id).first()
        if not user:
            await message.answer("❌ Siz ro'yxatdan o'tmagansiz!")
            return
        
        # Notificationlarni olish
        from apps.application.services.notification_service import notification_service
        notifications = notification_service.get_user_notifications(user, limit=10)
        
        if not notifications:
            await message.answer("📭 Sizda hali notificationlar yo'q")
            return
        
        # Notificationlarni ko'rsatish
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(
                text="📖 Barchasini o'qilgan deb belgilash",
                callback_data="mark_all_read"
            )
        )
        
        notification_text = "🔔 <b>Sizning notificationlaringiz:</b>\n\n"
        
        for i, notification in enumerate(notifications, 1):
            status = "✅" if notification.is_read else "🔔"
            notification_text += (
                f"{status} <b>{notification.title}</b>\n"
                f"📝 {notification.message[:100]}...\n"
                f"🕐 {notification.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
            )
        
        await message.answer(
            notification_text,
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        
    except Exception as e:
        await message.answer("❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.")

@notification_router.callback_query(F.data == "mark_all_read")
async def mark_all_notifications_read(callback: CallbackQuery):
    """Barcha notificationlarni o'qilgan deb belgilash"""
    try:
        user = BotUser.objects.filter(telegram_id=callback.from_user.id).first()
        if not user:
            await callback.answer("❌ Foydalanuvchi topilmadi!")
            return
        
        from apps.application.services.notification_service import notification_service
        count = notification_service.mark_all_notifications_as_read(user)
        
        await callback.answer(f"✅ {count} ta notification o'qilgan deb belgilandi!")
        
        # Yangilangan notificationlar ro'yxatini ko'rsatish
        await show_notifications(callback.message)
        
    except Exception as e:
        await callback.answer("❌ Xatolik yuz berdi!")

@notification_router.message(Command("clear_notifications"))
async def clear_notifications(message: Message):
    """Notificationlarni tozalash"""
    try:
        user = BotUser.objects.filter(telegram_id=message.from_user.id).first()
        if not user:
            await message.answer("❌ Siz ro'yxatdan o'tmagansiz!")
            return
        
        # Eski notificationlarni o'chirish (30 kundan eski)
        from django.utils import timezone
        from datetime import timedelta
        
        old_date = timezone.now() - timedelta(days=30)
        deleted_count = Notification.objects.filter(
            user=user,
            created_at__lt=old_date
        ).delete()[0]
        
        await message.answer(f"🗑️ {deleted_count} ta eski notification o'chirildi!")
        
    except Exception as e:
        await message.answer("❌ Xatolik yuz berdi!")

@notification_router.message(Command("notification_settings"))
async def notification_settings(message: Message):
    """Notification sozlamalari"""
    try:
        user = BotUser.objects.filter(telegram_id=message.from_user.id).first()
        if not user:
            await message.answer("❌ Siz ro'yxatdan o'tmagansiz!")
            return
        
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(
                text="🔔 Barcha xabarlar",
                callback_data="notif_all"
            )
        )
        builder.add(
            InlineKeyboardButton(
                text="📋 Faqat buyurtmalar",
                callback_data="notif_orders"
            )
        )
        builder.add(
            InlineKeyboardButton(
                text="📝 Faqat tenderlar",
                callback_data="notif_tenders"
            )
        )
        builder.add(
            InlineKeyboardButton(
                text="💳 Faqat to'lovlar",
                callback_data="notif_payments"
            )
        )
        
        await message.answer(
            "⚙️ <b>Notification sozlamalari</b>\n\n"
            "Qanday xabarlarni olishni xohlaysiz?",
            reply_markup=builder.as_markup(),
            parse_mode="HTML"
        )
        
    except Exception as e:
        await message.answer("❌ Xatolik yuz berdi!")

@notification_router.callback_query(F.data.startswith("notif_"))
async def handle_notification_settings(callback: CallbackQuery):
    """Notification sozlamalarini boshqarish"""
    try:
        setting = callback.data.split("_")[1]
        
        settings_text = {
            "all": "🔔 Barcha xabarlar",
            "orders": "📋 Faqat buyurtmalar", 
            "tenders": "📝 Faqat tenderlar",
            "payments": "💳 Faqat to'lovlar"
        }
        
        await callback.answer(f"✅ {settings_text.get(setting, 'Sozlama')} tanlandi!")
        
        # Bu yerda foydalanuvchining notification sozlamalarini saqlash mumkin
        # Hozircha faqat xabar ko'rsatamiz
        
    except Exception as e:
        await callback.answer("❌ Xatolik yuz berdi!")

@notification_router.message(Command("help_notifications"))
async def help_notifications(message: Message):
    """Notification yordam xabari"""
    help_text = (
        "🔔 <b>Notification yordam</b>\n\n"
        "<b>Mavjud buyruqlar:</b>\n"
        "/notifications - Notificationlaringizni ko'rish\n"
        "/clear_notifications - Eski notificationlarni tozalash\n"
        "/notification_settings - Notification sozlamalari\n"
        "/help_notifications - Bu yordam xabari\n\n"
        "<b>Notification turlari:</b>\n"
        "📋 Buyurtma yangilanishlari\n"
        "📝 Tender javoblari\n"
        "💳 To'lov muvaffaqiyati\n"
        "⚠️ Obuna muddati tugashiga eslatmalar\n"
        "🔔 Tizim xabarlari\n\n"
        "Notificationlar avtomatik ravishda yuboriladi va "
        "siz ularni bot orqali ko'rishingiz mumkin."
    )
    
    await message.answer(help_text, parse_mode="HTML")
