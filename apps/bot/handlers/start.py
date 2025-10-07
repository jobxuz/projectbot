from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Открыть",
            web_app={"url": f"https://uztextil.vercel.app"}
        )
    )
    await message.answer(
        "<b>Здравствуйте!</b>\n\n"
        "Вас приветствует бот №1 по проверенным и сертифицированным текстильным фабрикам Узбекистана.",
        parse_mode="HTML"
    )
    await message.answer_photo(
        photo=FSInputFile("welcome.jpg"),
        caption="Только проверенные и надёжные фабрики. Если условия не выполняются, действует гарантия возврата денег.",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    
