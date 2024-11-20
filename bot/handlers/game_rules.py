from aiogram import Router, types, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.utils.i18n import gettext as _
from aiogram.utils import formatting

from bot.keyboards.reply.menu import main_keyboard
from bot.core.config import settings
import pprint

router = Router(name="rules")

@router.message((F.text == "📜 规则") & (F.chat.type == ChatType.PRIVATE))
async def rules_handler(message: types.Message) -> None:
    """Rules message."""
    await message.answer(
        "规则",
        # formatting.Bold("规则").as_html,
    )
