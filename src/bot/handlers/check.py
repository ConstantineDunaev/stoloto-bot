from aiogram import Router
from aiogram.types import Message
from aiogram.utils.formatting import as_list, Bold, as_line, as_key_value, Text
from src.bot.filters import UserFilter
from src.database import Database
from src.config import Config
from src.utils import mask_from_values

check_router = Router()


async def check(text: str) -> Text:
    db = Database(Config.database_path)
    text = text.replace("-", " ")
    try:
        combination = [int(item) for item in text.split(" ")]
    except ValueError:
        raise RuntimeError("Не удалось извлечь значения комбинации")
    if len(combination) > 8:
        raise RuntimeError("Слишком много значений")
    if max(combination) > 20:
        raise RuntimeError("Неверный ввод - максимальное значение 20")
    if min(combination) < 1:
        raise RuntimeError("Неверный ввод - минимальное значение 1")
    left = combination[:4]
    right = combination[4:]
    if len(left) != len(set(left)):
        raise RuntimeError("Левая часть комбинации содержит повторяющиеся значения")
    if len(right) != len(set(right)):
        raise RuntimeError("Правая часть комбинации содержит повторяющиеся значения")

    lines = [as_line(Bold(f"Статистика комбинации {text}"))]
    if left:
        left_count_draws = await db.count_draws_with_left(mask_from_values(left))
        lines.append(as_line(as_key_value("Левое поле", left_count_draws)))
    if right:
        right_count_draws = await db.count_draws_with_right(mask_from_values(right))
        lines.append(as_line(as_key_value("Правое поле", right_count_draws)))

    return as_list(*lines)


@check_router.message(UserFilter())
async def check_handler(message: Message):
    try:
        text = await check(message.text)
        await message.answer(**text.as_kwargs())
    except Exception as e:
        text = f"Ошибка! {e}"
        await message.answer(text)
