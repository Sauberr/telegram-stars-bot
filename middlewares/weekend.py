from datetime import UTC, datetime
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message


def _is_weekend() -> bool:
    return datetime.now(UTC).weekday() in (5, 6)


class WeekendMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not _is_weekend():
            return await handler(event, data)


class WeekendCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        if not _is_weekend():
            return await handler(event, data)
        await event.answer("Bot does not work on weekends!", show_alert=True)
        return
