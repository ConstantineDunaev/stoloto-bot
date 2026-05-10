from aiogram import Router
from aiogram.types import Message
from src.bot.filters import UserFilter



start_router = Router()


@start_router.message(UserFilter())
async def start_handler(message: Message):
    await message.answer('test')
