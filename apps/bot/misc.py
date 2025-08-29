from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from django.conf import settings
from django.urls import reverse
import asyncio

from apps.bot.handlers.echo import echo_router
from apps.bot.handlers.start import start_router
from apps.bot.handlers.notification import notification_router

# Global instances
_dp = None
_bot = None


def get_dispatcher_and_bot() -> (Dispatcher, Bot):
    """Get or create global dispatcher and bot instances"""
    global _dp, _bot
    
    if _dp is None or _bot is None:
        _dp = Dispatcher()
        _dp.include_routers(
            start_router,
            echo_router,
            notification_router,
        )
        
        _bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    return _dp, _bot


def register_all_misc() -> (Dispatcher, Bot):
    """Legacy function for backward compatibility"""
    return get_dispatcher_and_bot()


async def bot_polling() -> None:
    """Start bot polling"""
    dp, bot = get_dispatcher_and_bot()
    await dp.start_polling(bot)


def get_webhook_url():
    host: str = settings.BOT_HOST
    if host.endswith("/"):
        host = host[:-1]
    return host + reverse("bot:webhook", args=(settings.BOT_TOKEN,))


async def start_webhook() -> None:
    """Start bot webhook"""
    dp, bot = get_dispatcher_and_bot()
    webhook_info = await bot.get_webhook_info()
    webhook_url = get_webhook_url()
    if webhook_url != webhook_info.url:
        await bot.set_webhook(
            url=webhook_url,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True
        )


def get_or_create_event_loop():
    """Get existing event loop or create new one"""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop
