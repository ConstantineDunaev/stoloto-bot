from dotenv import load_dotenv
from os import getenv
from pathlib import Path


class Config:
    load_dotenv()

    database_path = Path(getenv('DATABASE_PATH'))

    gosloto_parthner = getenv('GOSLOTO_PARTHNER')

    stoloto_game_name = getenv('STOLOTO_GAME_NAME')
    stoloto_draws_first_page = int(getenv('STOLOTO_DRAWS_FIRST_PAGE', 1))
    stoloto_draws_last_page = int(getenv('STOLOTO_DRAWS_LAST_PAGE', 300))
    stoloto_count_draws_on_page = int(getenv('STOLOTO_COUNT_DRAWS_ON_PAGE', 50))
    stoloto_delay = int(getenv('STOLOTO_DELAY', 20))

    telegram_token = getenv('TELEGRAM_TOKEN')
    telegram_users = [int(item.strip()) for item in getenv('TELEGRAM_USERS').split(',')]



