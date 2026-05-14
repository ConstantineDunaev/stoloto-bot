from aiosqlite import connect, Row
from pathlib import Path
from src.schemas import Draw, DrawsInfo


class Database:
    def __init__(self, database_path: Path):
        self.database_path = database_path

    async def init(self):
        sqls = """
            CREATE TABLE IF NOT EXISTS draw (
                draw_id INTEGER NOT NULL,
                number INTEGER NOT NULL,
                date date NOT NULL,
                super_prize INTEGER NOT NULL,
                combination TEXT NOT NULL,
                CONSTRAINT draw_pk PRIMARY KEY (draw_id)
            );
            CREATE INDEX IF NOT EXISTS draw_number_IDX ON draw (number);
            CREATE INDEX IF NOT EXISTS draw_id_IDX ON draw (draw_id);
            CREATE INDEX IF NOT EXISTS draw_date_IDX ON draw (date);
            CREATE TABLE IF NOT EXISTS combination (
                draw_id INTEGER NOT NULL,
                no INTEGER NOT NULL,
                value INTEGER NOT NULL
            );
            CREATE INDEX IF NOT EXISTS combination_draw_id_IDX ON combination (draw_id);
            CREATE INDEX IF NOT EXISTS combination_no_IDX ON combination (no);
            CREATE INDEX IF NOT EXISTS combination_value_IDX ON combination (value);
            CREATE INDEX IF NOT EXISTS unique_combination (
                combination_id INTEGER NOT NULL,
                lenght INTEGER NOT NULL,
                value INTEGER NOT NULL
            );
            CREATE INDEX IF NOT EXISTS combination_id_IDX ON unique_combination (combination_id);
            CREATE INDEX IF NOT EXISTS combination_lenght_IDX ON unique_combination (lenght);
            CREATE INDEX IF NOT EXISTS combination_value_IDX ON unique_combination (value);
        """
        async with connect(self.database_path) as connection:
            for sql in sqls.split(';'):
                await connection.execute(sql)

    async def write_draws(self, draws: list[Draw]):
        sql = "INSERT INTO draw (draw_id, number, date, super_prize, combination) VALUES (?, ?, ?, ?, ?)"
        parameters = [draw.as_tuple() for draw in draws]
        async with connect(self.database_path) as connection:
            await connection.executemany(sql, parameters)
            await connection.commit()

    async def write_combinations(self, combinations: list[tuple]):
        sql = "INSERT INTO combination (draw_id, no, value) VALUES (?, ?, ?)"
        async with connect(self.database_path) as connection:
            await connection.executemany(sql, combinations)
            await connection.commit()

    async def get_last_draw_id(self) -> int:
        sql = "SELECT max(draw_id) as last_draw_id FROM draw"
        async with connect(self.database_path) as connection:
            connection.row_factory = Row
            async with connection.cursor() as cursor:
                rows = await cursor.execute(sql)
                result = await rows.fetchone()
                last_draw_id = result['last_draw_id']
                return last_draw_id if last_draw_id else 0

    async def get_draws_info(self) -> DrawsInfo:
        sql = """
          SELECT 
              count(1) as total_count,
              min(number) as first_number,
              min(date) as first_date,
              max(number) as last_number,
              max(date) as last_date
          FROM draw d 
          """
        async with connect(self.database_path) as connection:
            connection.row_factory = Row
            async with connection.cursor() as cursor:
                rows = await cursor.execute(sql)
                result = await rows.fetchone()
                return DrawsInfo(**result)
