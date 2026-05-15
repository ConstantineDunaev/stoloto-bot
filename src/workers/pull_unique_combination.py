from src.database import Database
from src.config import Config
from src.utils import generate_combination
from asyncio import run


async def main():
    db = Database(Config.database_path)
    await db.init()
    for length in range(1, 5):
        combination = generate_combination(length)
        await db.write_unique_combinations(combination)

if __name__ == "__main__":
    run(main())
