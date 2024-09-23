from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.i18n import gettext as _

# from bot.keyboards.inline.menu import main_keyboard
from bot.keyboards.reply.menu import main_reply_keyboard

# from bot.services.analytics import analytics

router = Router(name="start")


@router.message(CommandStart())
# @analytics.track_event("Sign Up")
async def start_handler(message: types.Message) -> None:
    """欢迎消息."""
    await message.answer(
        text=_("💠 <b>使用 ListenGuardBot，您可以轻松查看任意群组中的消息。</b>\n\n🎯 单击<b>关键词</b>按钮来创建和管理您的关键词，单击<b>设置</b>来查看您的设置。"),  # noqa: E501
        reply_markup=main_reply_keyboard()
    )
