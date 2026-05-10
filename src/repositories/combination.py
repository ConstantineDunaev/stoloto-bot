from aiosqlite import connect
from pathlib import Path
from itertools import combinations
from json import dumps


class CombinationRepository:
    def __init__(self, database_path: Path):
        self.database_path = database_path

    async def init(self):
        sql = """
            CREATE TABLE IF NOT EXISTS combination (
                combination TEXT NOT NULL,
                CONSTRAINT combination_pk PRIMARY KEY (combination)
            )
        """
        async with connect(self.database_path) as connection:
            await connection.execute(sql)

    async def pull(self):
        values = [str(i).rjust(2, "0") for i in range(1, 21)]
        parameters = [(dumps(item),) for item in combinations(values, 4)]
        print(parameters)
        sql = "INSERT INTO combination (combination) VALUES (?) ON CONFLICT (combination) DO NOTHING"
        async with connect(self.database_path) as connection:
            await connection.executemany(sql, parameters)
            await connection.commit()

