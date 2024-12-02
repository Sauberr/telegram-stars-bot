import structlog
from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluent.runtime import FluentLocalization

from filters.is_owner import IsOwnerFilter

router = Router()
router.message.filter(F.chat.type == "private", IsOwnerFilter(is_owner=True))

logger = structlog.get_logger()


@router.message(Command("start"))
async def cmd_owner_hello(message: Message, l10n: FluentLocalization):
    await message.answer(l10n.format_value("hello-owner"))


@router.message(
    IsOwnerFilter(is_owner=True),
    Command(commands=["ping"]),
)
async def cmd_ping_bot(message: Message, l10n: FluentLocalization):
    await message.reply(l10n.format_value("ping-msg"))
