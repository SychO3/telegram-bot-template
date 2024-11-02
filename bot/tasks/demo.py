from aiogram import Bot
from loguru import logger


async def demo_task(bot: Bot) -> None:
    bot_info = await bot.get_me()
    name = bot_info.full_name
    logger.info(f"This is a demo task for {name}")
