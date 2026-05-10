from asyncio import run
from logging import getLogger, basicConfig
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.bot import start_bot
from src.config import Config
from src.workers.fill_draws import fill_draws
from datetime import datetime


async def main():
    session = AiohttpSession(proxy=Config.telegram_proxy)
    bot = Bot(token=Config.telegram_token,
              session=session)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=fill_draws,
                      trigger='interval',
                      seconds=Config.stoloto_draws_update_interval,
                      max_instances=1,
                      next_run_time=datetime.now(),
                      coalesce=True)
    await start_bot(scheduler, bot)


if __name__ == "__main__":
    logger = getLogger('main')

    loggers = ["aiosqlite", "urllib3", "asyncio", "tzlocal", "apscheduler"]
    for name in loggers:
        getLogger(name).propagate = False
    basicConfig(level='DEBUG', format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    try:
        run(main())
    except KeyboardInterrupt:
        logger.warning("Приложение принудительно остановлено")
    except Exception as e:
        logger.exception("Ошибка: %s", e)
