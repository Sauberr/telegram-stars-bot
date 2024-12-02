import structlog
from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import InlineKeyboardMarkup, LabeledPrice, Message, PreCheckoutQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluent.runtime import FluentLocalization

router = Router()
router.message.filter(F.chat.type == "group")

logger = structlog.get_logger()


@router.message(F.content_type.in_({"new_chat_members", "left_chat_member"}))
async def on_user_join_or_left(message: Message):
    await message.delete()
