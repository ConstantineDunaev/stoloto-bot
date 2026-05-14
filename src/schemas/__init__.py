from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from json import dumps


class Draw(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )
    draw_id: int = Field(alias="id")
    number: int
    date: datetime
    super_prize: int = Field(alias="superPrize")
    winning_combination: list[str] = Field(alias="winningCombination")

    def as_tuple(self) -> tuple[int, int, datetime, int, str]:
        return self.draw_id, self.number, self.date, self.super_prize, dumps(self.winning_combination)

    def combinations(self) -> list[tuple[int, int, int]]:
        return [(self.draw_id, index, int(item))
                for index, item in enumerate(self.winning_combination, start=1)]


class ArchiveResponse(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
    )
    draws: list[Draw]


class DrawsInfo(BaseModel):
    total_count: int
    first_number: int
    first_date: datetime
    last_number: int
    last_date: datetime
