from src.stoloto import get_arhive_draws
from src.repositories import DrawRepository
from asyncio import run, sleep
from requests.exceptions import HTTPError
from logging import getLogger, basicConfig
from src.config import Config


logger = getLogger('stoloto')


async def fill_draws():
    db = DrawRepository(Config.database_path)
    await db.init()
    last_id = await db.get_last_draw_id()
    logger.debug('ID последнего тиража: %d', last_id)
    for page in range(Config.stoloto_draws_first_page, Config.stoloto_draws_last_page + 1):
        logger.debug('Получение страницы №%d...', page)
        for attemtp in range(1, 6):
            try:
                draws = get_arhive_draws(page=page)
                draws = [draw for draw in draws if draw.id > last_id]
                if not draws:
                    return
                await db.write_draws(draws)
                await sleep(Config.stoloto_delay)
                break
            except HTTPError as e:
                logger.exception('Ошибка получения данных тиража: page = %d, attempt = %d', page, attemtp)
                await sleep(30)


if __name__ == "__main__":
    loggers = ["aiosqlite", "urllib3", "asyncio"]
    for name in loggers:
        getLogger(name).propagate = False
    basicConfig(level='DEBUG', format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    run(fill_draws())
