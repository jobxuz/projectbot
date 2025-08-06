# bot/handlers.py
from aiogram import Router, types
from apps.user.models import User
from aiogram.filters import CommandStart
from asgiref.sync import sync_to_async


router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message):
    print("start bosildi")
    await sync_to_async(User.objects.get_or_create)(
        telegram_id=message.from_user.id,
        defaults={
            "telegram_username": message.from_user.username,
        },
    )
    await message.answer("Assalomu alaykum! Botga xush kelibsiz.")
