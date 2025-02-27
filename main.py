import logging
import asyncio
from aiogram import Bot, Dispatcher, types


from handlers import all_handlers
from dbdb.database import init_db
from config_.config import Config, load_config


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] #%(levelname)-8s %(filename)-15s: %(lineno)-4s - %(message)s')
    #    format='%(filename)-15s: %(lineno)-4s #%(levelname)-8s '
    #           '[%(asctime)s] - %(message)s')
    # format='%(filename)-15s: %(lineno)-5s #%(levelname)-8s '
    #           '[%(asctime)s] - %(name)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info('Загрузка конфига в переменную config')
    config: Config = load_config()

    logger.info('Инициализация базы данных, запуск init_db() ')
    init_db()

    logger.info('инициализируем бот и диспетчер')
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    # регистриуем роутеры в диспетчере - на будущее в основном
    logger.info('регистриуем роутеры в диспетчере')
    dp.include_router(all_handlers.router)

    logger.info('удаляем апдейты, запуск polling')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
