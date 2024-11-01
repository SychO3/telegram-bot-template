from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_keyboard() -> InlineKeyboardMarkup:
    """Use in main menu."""
    buttons = [
        [InlineKeyboardButton(text=_("钱包按钮"), callback_data="wallet")],
        [InlineKeyboardButton(text=_("会员按钮"), callback_data="premium")],
        [InlineKeyboardButton(text=_("信息按钮"), callback_data="info")],
        [InlineKeyboardButton(text=_("支持按钮"), callback_data="support")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    keyboard.adjust(1, 1, 2)

    return keyboard.as_markup()
