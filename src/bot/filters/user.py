from aiogram.filters import BaseFilter
from aiogram.types import User
from src.config import Config


class UserFilter(BaseFilter):
    async def __call__(self, *args, **kwargs):
        user = kwargs.get("event_from_user")
        if not isinstance(user, User):
            return False

        return user.id in Config.telegram_users
