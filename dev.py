from src.stoloto import Stoloto
from src.database import Database
from src.config import Config


async def main():
    stoloto = Stoloto(Config.gosloto_parthner)
    db = Database(Config.database_path)
    await db.init()
    draws = stoloto.get_arhive_draws(page=1,
                                     count=Config.stoloto_count_draws_on_page,
                                     game=Config.stoloto_game_name)
    combinations = [combination for draw in draws for combination in draw.combinations()]
    await db.write_draws(draws)
    await db.write_combinations(combinations)


if __name__ == "__main__":
    from asyncio import run

    run(main())