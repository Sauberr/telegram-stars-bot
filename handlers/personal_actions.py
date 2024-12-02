from datetime import datetime, timedelta, timezone
from itertools import count
from pydoc import plainpager

import inflect
import structlog
from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluent.runtime import FluentLocalization

router = Router()
router.message.filter(F.chat.type == "private")

logger = structlog.get_logger()


@router.message(Command("start"))
async def cmd_owner_hello(message: Message, l10n: FluentLocalization):
    await message.answer(l10n.format_value("hello-msg"))


@router.message(F.content_type.in_({"photo", "video"}))
async def cmd_media_react_bot(message: Message, l10n: FluentLocalization):
    await message.reply(l10n.format_value("media-msg"))


@router.message(Command("donate", "donat", "донат"))
async def cmd_donate(
    message: Message, command: CommandObject, l10n: FluentLocalization
):
    if (
        command.args is None
        or not command.args.isdigit()
        or not 1 <= int(command.args) <= 2500
    ):
        await message.answer(l10n.format_value("donate-input-error"))
        return

    amount = int(command.args)
    plurals = inflect.engine()
    count_stars = plurals.plural("star", amount)
    kb = InlineKeyboardBuilder()
    kb.button(text=l10n.format_value("donate-button-pay", {"amount": amount}), pay=True)
    kb.button(
        text=l10n.format_value("donate-button-cancel"), callback_data="donate_cancel"
    )
    kb.adjust(1)
    prices = [LabeledPrice(label="XTR", amount=amount)]
    readable_timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    payload = f"{amount}_{count_stars}_{readable_timestamp}"

    await message.answer_invoice(
        title=l10n.format_value("donate-invoice-title"),
        description=l10n.format_value("donate-invoice-description", {"amount": amount}),
        prices=prices,
        provider_token="410694247:TEST:11b24e76-d548-4cbd-bdba-2a98f9da474e",
        payload=payload,
        currency="XTR",
        reply_markup=kb.as_markup(),
    )


@router.callback_query(F.data == "donate_cancel")
async def on_donate_cancel(callback: CallbackQuery, l10n: FluentLocalization):
    await callback.answer(l10n.format_value("donate-cancel-payment"))

    await callback.message.delete()


@router.message(Command("paysupport"))
async def cmd_paysupport(message: Message, l10n: FluentLocalization):
    await message.answer(l10n.format_value("donate-paysupport-message"))


@router.message(Command("refund"))
async def cmd_refund(
    message: Message, bot: Bot, command: CommandObject, l10n: FluentLocalization
):
    transaction_id = command.args

    if transaction_id is None:
        await message.answer(l10n.format_value("donate-refund-input-error"))
        return

    try:
        amount, count_stars, purchase_date = transaction_id.split("_")
        amount = int(amount)
        transaction_timestamp = datetime.strptime(
            purchase_date, "%Y-%m-%d %H:%M:%S UTC"
        )
    except (ValueError, TypeError):
        await message.answer(l10n.format_value("donate-refund-invalid-transaction"))
        return

    current_time = datetime.now(timezone.utc)
    time_since_purchase = current_time - transaction_timestamp

    if time_since_purchase > timedelta(days=14):
        await message.answer(l10n.format_value("donate-refund-time-expired"))
        return

    try:
        await bot.refund_star_payment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=transaction_id,
        )
        await message.answer(l10n.format_value("donate-refund_success"))
    except TelegramBadRequest as e:
        error_text = l10n.format_value("donate-refund-code-not-found")

        if "CHARGE_ALREADY_REFUNDED" in e.message:
            error_text = l10n.format_value("donate-refund-already-refunded")

        await message.answer(error_text)


@router.pre_checkout_query()
async def pre_checkout_query(query: PreCheckoutQuery, l10n: FluentLocalization):
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def on_successful_payment(message: Message, l10n: FluentLocalization):
    await message.answer(
        l10n.format_value(
            "donate-successful-payment",
            {"transaction_id": message.successful_payment.invoice_payload},
        ),
        message_effect_id="5159385139981059251",
    )
