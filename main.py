
import asyncio
from aiogram import Bot, Dispatcher


from handlers import all_handlers
# from db.database_v2 import init_db

# предыдущая версия
from db.old_database import init_db
from config import Config, load_config, logger


async def main():

    logger.info('Загрузка конфига в переменную config')
    config: Config = load_config()

    logger.info('Инициализация базы данных')
    await init_db()

    logger.info('инициализируем бот и диспетчер')
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    logger.info('регистриуем роутеры в диспетчере')
    dp.include_router(all_handlers.router)

    logger.info('удаляем апдейты, запуск polling')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("stop bot")
