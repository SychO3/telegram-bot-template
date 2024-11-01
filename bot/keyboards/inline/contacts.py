from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.core.config import settings


def contacts_keyboard() -> InlineKeyboardMarkup:
    """Use when call contacts command."""
    buttons = [
        [InlineKeyboardButton(text=_("联系按钮"), url=settings.SUPPORT_URL)],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    return keyboard.as_markup()


def support_keyboard() -> InlineKeyboardMarkup:
    """Use when call support query."""
    buttons = [
        [InlineKeyboardButton(text=_("支持按钮"), url=settings.SUPPORT_URL)],
        [InlineKeyboardButton(text=_("后退按钮"), callback_data="menu")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    return keyboard.as_markup()
