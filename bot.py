import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.loader import load_config, Config
from database.setup import create_engine, create_session_pool
from tgbot.handlers import routers_list
from tgbot.logger import setup_logging
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.database import DatabaseMiddleware


def register_global_middlewares(dp: Dispatcher, config: Config, session_pool=None):
    middleware_types = [
        ConfigMiddleware(config),
        DatabaseMiddleware(session_pool),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


async def main():
    setup_logging()

    config = load_config(".env")
    storage = MemoryStorage()

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML, link_preview_is_disabled=True
        ),
    )
    # await bot.delete_webhook()

    dp = Dispatcher(storage=storage)
    dp["config"] = config

    dp.include_routers(*routers_list)

    engine = create_engine(db=config.db)
    session_pool = create_session_pool(engine=engine)

    register_global_middlewares(dp, config, session_pool)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot was stopped")
