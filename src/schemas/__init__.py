from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from json import dumps


class Draw(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )
    id: int
    number: int
    date: datetime
    super_prize: int = Field(alias="superPrize")
    winning_combination: list[str] = Field(alias="winningCombination")

    @property
    def combination(self) -> str:
        return dumps(self.winning_combination)

    @property
    def left_field(self) -> str:
        return dumps(sorted(self.winning_combination[:4]))

    @property
    def right_field(self) -> str:
        return dumps(sorted(self.winning_combination[4:]))


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
