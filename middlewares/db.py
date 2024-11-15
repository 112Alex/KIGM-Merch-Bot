from typing import Any, Awaitable, Dict
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool


    async def __call__(
        self,
        handler: callable[[TelegramObject, Dict[str, Any ]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data['session'] = session
            return await handler(event, data)