from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.formatting import Text
from src.bot.filters import UserFilter
from src.bot.keyboards.reply import START_KEYBOARD

start_router = Router()


@start_router.message(CommandStart(), UserFilter())
async def start_handler(message: Message):
    text = Text("Анализ комбинаций Спортлото 4x20")
    await message.answer(**text.as_kwargs(),
                         reply_markup=START_KEYBOARD)
