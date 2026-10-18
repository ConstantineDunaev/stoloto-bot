from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from json import dumps
from src.utils import mask_from_values


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

    @property
    def left_mask(self) -> int:
        return mask_from_values([int(value) for value in self.winning_combination[:4]])

    @property
    def right_mask(self) -> int:
        return mask_from_values([int(value) for value in self.winning_combination[4:]])

    def as_tuple(self) -> tuple[int, int, datetime, int, str, int, int]:
        return (self.draw_id, self.number, self.date, self.super_prize,
                dumps(self.winning_combination), self.left_mask, self.right_mask)


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
