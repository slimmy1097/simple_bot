
import aiosqlite
import os
import asyncio

from config import load_config, logger


DB_PATH = load_config().DB_PATH


async def init_db():
    if not os.path.exists(DB_PATH):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    city TEXT,
                    birth_date TEXT,
                    email TEXT
                )
            ''')
            await db.commit()
    logger.info('База данных создана')


async def user_exists(user_id):
    logger.info(f'Функция user_exists вызвана с user_id = {user_id}')
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT user_id FROM users WHERE user_id = ?',
                              (user_id,)) as cursor:
            user = await cursor.fetchone()
        if not user:
            logger.info(f'''Не нашли пользователя {user_id} 
                        \t\t\t\tи записываем его в БД''')
            await db.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
            await db.commit()

    return user is not None


async def add_user(user_id, username, first_name, last_name, city, birth_date, email):
    logger.info(f'Добавляем пользователя {user_id} в базу данных')
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT INTO users (user_id, username, first_name, last_name, city, birth_date, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET 
                username = excluded.username,
                first_name = excluded.first_name,
                last_name = excluded.last_name,
                city = excluded.city,
                birth_date = excluded.birth_date,
                email = excluded.email
        ''', (user_id, username, first_name, last_name, city, birth_date, email))

        await db.commit()
    logger.info(f'Добавлен новый пользователь: {user_id}')


async def get_user(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)) as cursor:
            user = await cursor.fetchone()
    logger.info(f'Получаем данные пользователя {user_id}')

    if user:
        # user_id, username, first_name, last_name, city, birth_date, email
        response_from_db = (f'''Информация о пользователе {user[1]}:
                Имя: {user[2]}
                Фамилия: {user[3]}
                Город: {user[4]}
                Дата рождения: {user[5]}
                email: {user[6]}
              ''')

    else:
        response_from_db = (f'Пользователь с ID {user_id} не найден')

    return response_from_db


# # for pytest
# async def main():
#     await init_db()

#     user_id = 123
#     exists = await user_exists(user_id)
#     if not exists:
#         await add_user(user_id, 'nickname', 'name', 'family', 'vrn', '2000-01-01', 'for@mail.com')

#     user = await get_user(user_id)
#     if user:
#         print(f'Пользователь найден: {user}')
#     else:
#         print('Пользователь не найден')


# # Запуск асинхронного кода
# if __name__ == '__main__':
#     asyncio.run(main())
