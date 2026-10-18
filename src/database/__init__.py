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
                left_mask INTEGER NOT NULL,
                right_mask INTEGER NOT NULL,
                CONSTRAINT draw_pk PRIMARY KEY (draw_id)
            );
            CREATE INDEX IF NOT EXISTS draw_number_IDX ON draw (number);
            CREATE INDEX IF NOT EXISTS draw_id_IDX ON draw (draw_id);
            CREATE INDEX IF NOT EXISTS draw_date_IDX ON draw (date);
        """
        async with connect(self.database_path) as connection:
            for sql in sqls.split(';'):
                await connection.execute(sql)

    async def write_draws(self, draws: list[Draw]):
        sql = ("INSERT INTO draw (draw_id, number, date, super_prize, combination, left_mask, right_mask) "
               "VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT (draw_id) DO NOTHING")
        parameters = [draw.as_tuple() for draw in draws]
        async with connect(self.database_path) as connection:
            await connection.executemany(sql, parameters)
            await connection.commit()

    async def count_draws_with_left(self, mask: int) -> int:
        sql = "SELECT count(*) as cnt FROM draw WHERE (left_mask & ?) = ?"
        async with connect(self.database_path) as connection:
            connection.row_factory = Row
            async with connection.cursor() as cursor:
                rows = await cursor.execute(sql, (mask, mask))
                result = await rows.fetchone()
                return result['cnt']

    async def count_draws_with_right(self, mask: int) -> int:
        sql = "SELECT count(*) as cnt FROM draw WHERE (right_mask & ?) = ?"
        async with connect(self.database_path) as connection:
            connection.row_factory = Row
            async with connection.cursor() as cursor:
                rows = await cursor.execute(sql, (mask, mask))
                result = await rows.fetchone()
                return result['cnt']

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
