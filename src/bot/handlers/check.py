from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.formatting import as_list, Bold, as_line, as_key_value
from src.bot.filters import UserFilter
from src.repositories import DrawRepository
from src.config import Config
from re import compile

check_router = Router()
pattern = compile(r"\d+")


@check_router.message(UserFilter())
async def check_handler(message: Message):
    repository = DrawRepository(Config.database_path)
    combination = [int(item) for item in pattern.findall(message.text)]
    if len(combination) == 0:
        raise RuntimeError("Не удалось извлечь значения комбинации")
    if len(combination) > 8:
        raise RuntimeError("Слишком много значений")
    if max(combination) > 20:
        raise RuntimeError("Неверный ввод - максимальное значение 20")
    if min(combination) < 1:
        raise RuntimeError("Неверный ввод - минимальное значение 1")
    combination = [str(item).rjust(2, "0") for item in combination]
    left = combination[:4]
    right = combination[4:]
    if len(left) != len(set(left)):
        raise RuntimeError("Левая часть комбинации содержит повторяющиеся значения")
    if len(right) != len(set(right)):
        raise RuntimeError("Правая часть комбинации содержит повторяющиеся значения")
    print(combination)
