import logging
import asyncio
from aiogram import Bot, Dispatcher, types

import sqlite3
from handlers import all_handlers

from config_.config import Config, load_config
# from handlers import other_handlers, user_handlers

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    # Инициализация бота и диспетчера
    logger.info('загрузка конфига в переменную config')
    config: Config = load_config()

    logger.info('инициализируем бот и диспетчер')
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    # регистриуем роутеры в диспетчере - на будущее в основном
    logger.info('регистриуем роутеры в диспетчере')
    dp.include_router(all_handlers.router)

    logger.info('удаляем апдейты, запуск polling')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
