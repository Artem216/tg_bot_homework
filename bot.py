import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from src.config import load_config
# from src.filters.admin import AdminFilter
# from src.handlers.admin import register_admin
from src.handlers.user import register_user
# from src.middlewares.environment import EnvironmentMiddleware

# from tgbot.db import Base, engine

# from tgbot.services import credentials, client, sheet 

# from tgbot.server import create_app


logger = logging.getLogger(__name__)





def register_all_handlers(dp):
    register_user(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")



    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    

    bot['config'] = config

    register_all_handlers(dp)
    

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        # Base.metadata.create_all(engine)
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
