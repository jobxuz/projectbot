import asyncio
import django
import os
import sys
import environ



sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(__file__), '.env'))



from aiogram import Bot, Dispatcher
from apps.bot.handlers import router


BOT_TOKEN = env("BOT_TOKEN")



async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
