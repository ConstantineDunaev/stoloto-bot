from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.bot.handlers import main_router


async def start_bot(scheduler: AsyncIOScheduler, bot: Bot):
    scheduler.start()

    storage = MemoryStorage()

    dp = Dispatcher(storage=storage)
    dp.include_router(main_router)

    allowed_updates = ["message"]
    await dp.start_polling(bot, allowed_updates=allowed_updates)
