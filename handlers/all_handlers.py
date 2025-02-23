from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

import sqlite3

import logging
logger = logging.getLogger(__name__)
# Инициализируем форматтер
formatter_3 = logging.Formatter(
    fmt='#%(levelname)-8s [%(asctime)s] - %(message)s'
)


# init router in that module
router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Страт здесь. Простой эхо-бот')


@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='Помощь, но её нет')


# Функция для проверки наличия пользователя в базе данных
def user_exists(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


# Функция для добавления пользователя в базу данных
def add_user(user_id, first_name, last_name, username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (id, first_name, last_name, username) VALUES (?, ?, ?, ?)',
                   (user_id, first_name, last_name, username))
    conn.commit()
    conn.close()


# Обработчик команды /start и любого текстового сообщения
@router.message(Command(commands=['start']))
@router.message()
async def echo(message: Message):
    logging.info(f'User {message.from_user.id} started the bot.')
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    if not user_exists(user_id):
        add_user(user_id, first_name, last_name, username)
        await message.answer(f"Привет, {first_name}! Ты был добавлен в базу данных.")
    else:
        await message.answer(f"Привет, {first_name}! Ты уже есть в базе данных.")

    # Эхо-ответ
    await message.answer(message.text)


@router.message()
async def send_echo(message: Message):
    logger.info('enter in send_echo')
    try:
        print(message)
        print(message)
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='другой какой-то тип апдейтов')
