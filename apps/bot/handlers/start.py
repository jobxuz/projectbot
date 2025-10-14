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
        "Здравствуйте Вас приветствует texverified - первый телеграмм апп верифицированный текстильных фабрик Узбекистана.",
        parse_mode="HTML"
    )
    await message.answer_photo(
        photo=FSInputFile("welcome.jpg"),
        caption="Тут вы найдете только проверенных производителей по нужному Вам сегменту.",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    
