from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.formatting import as_line, as_list, Bold, Code
from src.bot.filters import UserFilter
from src.bot.keyboards.reply import START_KEYBOARD

start_router = Router()


@start_router.message(CommandStart(), UserFilter())
async def start_handler(message: Message):
    text = as_list(
        as_line(Bold("Анализ комбинаций Спортлото 4x20")),
        as_line("Что бы проверить комбинацию отправьте набор чисел от 1 до 20, разделенных знаком -"),
        as_line("Примеры:"),
        as_line(Code("20-12")),
        as_line(Code("20-12-15")),
        as_line(Code("20-12-15-1")),
        as_line(Code("20-12-15-1-12-19")),
        as_line(Code("20-12-15-1-12-19-8")),
        as_line(Code("20-12-15-1-12-19-8-3")),
    )
    await message.answer(**text.as_kwargs(),
                         reply_markup=START_KEYBOARD)
