from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.i18n import gettext as _

from bot.keyboards.reply.menu import main_keyboard
from bot.core.config import settings

router = Router(name="start")


@router.message(CommandStart())
# @analytics.track_event("Sign Up")
async def start_handler(message: types.Message) -> None:
    """Welcome message."""
    await message.answer(_("欢迎使用 pc28 机器人！"), reply_markup=main_keyboard())
    print(settings)
