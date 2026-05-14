from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.formatting import as_list, Bold, as_line, as_key_value
from src.bot.filters import UserFilter
from src.database import Database
from src.config import Config

draws_router = Router()


@draws_router.message(UserFilter(), F.text == "📊 Тиражи")
async def draw_handler(message: Message):
    repository = Database(Config.database_path)
    draws_info = await repository.get_draws_info()
    text = as_list(
        as_line(Bold("📊 Информация о тиражах")),
        as_line(as_key_value("Количество тиражей", draws_info.total_count)),
        as_line(as_key_value("Первый тираж",
                             f"№{draws_info.first_number} от {draws_info.first_date.strftime("%d.%m.%Y %H:%M")}")),
        as_line(as_key_value("Последний тираж",
                             f"№{draws_info.last_number} от {draws_info.last_date.strftime("%d.%m.%Y %H:%M")}"))
    )
    await message.answer(**text.as_kwargs())
