from src.stoloto import Stoloto
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

    stoloto = Stoloto(Config.gosloto_parthner)

    for page in range(Config.stoloto_draws_first_page, Config.stoloto_draws_last_page + 1):
        logger.debug('Получение страницы №%d...', page)
        for attempt in range(1, 6):
            try:
                draws = stoloto.get_arhive_draws(page=page,
                                                 count=Config.stoloto_count_draws_on_page,
                                                 game=Config.stoloto_game_name)
                draws = [draw for draw in draws if draw.id > last_id and draw.winning_combination]
                if not draws:
                    logger.debug('Нет новых тиражей')
                    return
                await db.write_draws(draws)
                count_draws = len(draws)
                logger.debug('Получено новых тиражей: %d', count_draws)
                if count_draws == Config.stoloto_count_draws_on_page:
                    await sleep(Config.stoloto_delay)
                else:
                    return
                break
            except HTTPError as e:
                logger.exception('Ошибка получения данных тиража: page = %d, attempt = %d', page, attempt)
                await sleep(Config.stoloto_delay * attempt)


if __name__ == "__main__":
    loggers = ["aiosqlite", "urllib3", "asyncio"]
    for name in loggers:
        getLogger(name).propagate = False
    basicConfig(level='DEBUG', format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    run(fill_draws())
