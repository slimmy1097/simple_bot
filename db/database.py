import sqlite3
import logging
import os.path

logger = logging.getLogger(__name__)


# Функция для создания базы данных и таблицы пользователей
def init_db():
    if not os.path.exists('db/users.db'):
        conn = sqlite3.connect('dbdb/users.db')
        cursor = conn.cursor()

        cursor.execute('''
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

    conn.commit()
    conn.close()
    logger.info('База данных инициализирована')


def user_exists(user_id):
    logger.info(f'Функция user_exists вызвана с user_id = {user_id}')
    conn = sqlite3.connect('dbdb/users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    logger.info(f'''
                Ищем пользователя {user_id} в БД
                и {('не находим', 'находим его')[user is not None]}''')

    conn.close()
    return user is not None


def add_user(user_id, username, first_name, last_name, city, birth_date, email):
    logger.info(f'Добавляем пользователя в базу данных')
    conn = sqlite3.connect('dbdb/users.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO users (user_id, username, first_name, last_name, city, birth_date, email)
        VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                   (user_id, username, first_name, last_name, city, birth_date, email))

    conn.commit()
    conn.close()
    logger.info(f'Добавлен новый пользователь: {user_id}')
