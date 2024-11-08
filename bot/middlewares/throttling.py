from __future__ import annotations
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, Update
from cachetools import TTLCache

from bot.core.config import settings


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = settings.RATE_LIMIT) -> None:
        self.cache: TTLCache[int, None] = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
            self,
            handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
            event: Any,
            data: dict[str, Any],
    ) -> Any:
        if isinstance(event, Message):
            chat_id = event.chat.id
        elif isinstance(event, CallbackQuery):
            chat_id = event.message.chat.id if event.message else event.from_user.id
        elif isinstance(event, Update):
            chat_id = event.message.chat.id if event.message else 0
        else:
            return await handler(event, data)

        if chat_id != 0:
            self.cache[chat_id] = None
            return await handler(event, data)

        return None
