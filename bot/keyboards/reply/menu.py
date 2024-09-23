from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_reply_keyboard() -> ReplyKeyboardMarkup:
    """Use in main menu."""
    buttons = [
        [KeyboardButton(text=_("🔑\n关键词"))],
        # [KeyboardButton(text=_("👤️ 我的信息"))],
        [KeyboardButton(text=_("👥\n推荐"))],
        [KeyboardButton(text=_("⁉️\n帮助"))],
        [KeyboardButton(text=_("💳\n订阅"))],
        [KeyboardButton(text=_("⚙️\n设置"))],
    ]

    keyboard = ReplyKeyboardBuilder(markup=buttons)

    keyboard.adjust(1, 2, 2)

    return keyboard.as_markup()
