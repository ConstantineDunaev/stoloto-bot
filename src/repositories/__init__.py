from aiosqlite import connect
from pathlib import Path
from src.schemas import Draw


class DrawRepository:
    def __init__(self, database_path: Path):
        self.database_path = database_path

    async def init(self):
        sqls = """
            CREATE TABLE IF NOT EXISTS draw (
                id INTEGER NOT NULL,
                "number" INTEGER NOT NULL,
                date date NOT NULL,
                super_prize INTEGER NOT NULL,
                combination TEXT NOT NULL, left_field TEXT NOT NULL, right_field TEXT,
                CONSTRAINT draw_pk PRIMARY KEY (id)
            );
            
            CREATE INDEX IF NOT EXISTS draw_number_IDX ON draw ("number");
            CREATE INDEX IF NOT EXISTS draw_id_IDX ON draw (id);
            CREATE INDEX IF NOT EXISTS draw_date_IDX ON draw (date);
            CREATE INDEX IF NOT EXISTS draw_left_field_IDX ON draw (left_field);
            CREATE INDEX IF NOT EXISTS draw_right_field_IDX ON draw (right_field);
        """
        async with connect(self.database_path) as connection:
            for sql in sqls.split(';'):
                await connection.execute(sql)

    async def write_draws(self, draws: list[Draw]):
        sql = ("INSERT INTO draw (id, number, date, super_prize, combination, left_field, right_field) "
               "VALUES (?, ?, ?, ?, ?, ?, ?)")
        parameters = [(draw.id, draw.number, draw.date, draw.super_prize, draw.combination, draw.left_field, draw.right_field)
                      for draw in draws]
        async with connect(self.database_path) as connection:
            await connection.executemany(sql, parameters=parameters)
            await connection.commit()

    async def get_last_draw_id(self) -> int:
        sql = "SELECT max(id) FROM draw"
        async with connect(self.database_path) as connection:
            async with connection.cursor() as cursor:
                rows = await cursor.execute(sql)
                result = await rows.fetchone()
                last_id = result[0]
                return last_id if last_id else 0
