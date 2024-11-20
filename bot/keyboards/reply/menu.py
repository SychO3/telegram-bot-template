from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text=_("📝 注单")), KeyboardButton(text=_("💵 流水"))],
        [KeyboardButton(text=_("🎉 开奖结果")), KeyboardButton(text=_("📜 规则"))],
        [KeyboardButton(text=_("⬆️ 上下分群")), KeyboardButton(text=_("💰 投注群"))],
    ]
    keyboard = ReplyKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()

