from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.i18n import gettext as _

from bot.keyboards.reply.menu import main_keyboard

router = Router(name="start")


@router.message(CommandStart())
# @analytics.track_event("Sign Up")
async def start_handler(message: types.Message) -> None:
    """Welcome message."""
    await message.answer(_("欢迎使用 pc28 机器人！"), reply_markup=main_keyboard())



@router.message()
async def echo(message: types.Message) -> None:
    """Echo message."""

    print(f"message.dice: {message.dice}")

    await message.answer(str(message.dice.value))