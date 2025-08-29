from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
from django.conf import settings

start_router = Router()

@start_router.message(CommandStart())
async def command_start_handler(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="🌐 Ochish",
            web_app={"url": f"{getattr(settings, 'WEBAPP_URL', 'https://uztextil.vercel.app')}"}
        )
    )
    
    await message.answer(
        "<b>Assalomu aleykum!</b>\n\n"
        "Sizni O'zbekistondagi tasdiqlangan,\ntekshirilgan tekstil fabrikalari bo'yicha\n1-raqamli bot kutib oladi.\n\n"
        "🔔 <b>Notification buyruqlari:</b>\n"
        "/notifications - Xabarlaringizni ko'rish\n"
        "/help_notifications - Yordam",
        parse_mode="HTML"
    )
    
    await message.answer_photo(
        photo=FSInputFile("static/images/welcome.png"),
        caption="Faqat oraliqsiz, ishonchli fabrikalar.\nAgar shartlar bajarilmasa, pulni qaytarib\nberish kafolati mavjud",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    
