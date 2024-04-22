import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.settings import settings
from app.routers import register_all_routers
from app import logging

import asyncio


async def main():

    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True))
    dp = Dispatcher()

    # Регистрация обработчиков
    register_all_routers(dp)
    await logging.setup()
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
