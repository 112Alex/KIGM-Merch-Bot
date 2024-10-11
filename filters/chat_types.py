from aiogram.filters import Filter
from aiogram import Bot, types

from common.variables import ADMIN_LIST


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, msg: types.Message) -> bool:
        return msg.chat.type in self.chat_types

class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, msg: types.Message, bot: Bot) -> bool:
        return msg.from_user.id in ADMIN_LIST