from __future__ import annotations
from typing import TYPE_CHECKING

from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeChat

from bot.database.database import sessionmaker
from bot.services.users import get_admin_ids

if TYPE_CHECKING:
    from aiogram import Bot

users_commands: dict[str, dict[str, str]] = {
    "en": {
        "start": "start bot",
    },
    "zh": {
        "start": "开始使用",
    },
}

admins_commands: dict[str, dict[str, str]] = {
    **users_commands,
    "en": {
        "admin": "admin panel",
    },
    "zh": {
        "admin": "管理员面板",
    },
}


async def set_default_commands(bot: Bot) -> None:
    await remove_default_commands(bot)

    for language_code in users_commands:
        await bot.set_my_commands(
            [
                BotCommand(command=command, description=description)
                for command, description in users_commands[language_code].items()
            ],
            scope=BotCommandScopeAllPrivateChats(),
        )

        # Commands for admins
        async with sessionmaker() as session:
            admin_ids = await get_admin_ids(session)
            for admin_id in admin_ids:
                await bot.set_my_commands(
                    [
                        BotCommand(command=command, description=description)
                        for command, description in admins_commands[language_code].items()
                    ],
                    scope=BotCommandScopeChat(chat_id=admin_id),
                )


async def remove_default_commands(bot: Bot) -> None:
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
