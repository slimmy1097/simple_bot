
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup

from db.database import user_exists, add_user

import logging
logger = logging.getLogger(__name__)


# init router in that module
router = Router()


# all states for registration step
class Registration(StatesGroup):
    first_name = State()
    last_name = State()
    city = State()
    birth_date = State()
    email = State()
    end_update = State()


@router.message(StateFilter(default_state), ~Command('start'))
async def first_enter(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or ''

    logger.info(f'Самый первый вход, {user_id} еще не создавался')
    if not await user_exists(user_id):
        await message.answer(
            'Привет!\nДавай зарегистрируем тебя\n\nДля регистрации /start')


@router.message(StateFilter(default_state), Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or ''

    logger.info('выбрана команда /start, выполняется cmd_start')
    if await user_exists(user_id):
        logger.info(
            f'пользователь есть в базе\n{user_id=} {username=}')
        await message.send_copy(chat_id=message.chat.id)
        return

    if not message.from_user.first_name or not message.from_user.last_name:
        logger.info(
            'у пользователя в профиле не заполнены first_name и last_name')
        await message.answer('Для регистрации в системе, введите, пожалуйста, ваше имя:')
        await state.set_state(Registration.first_name)
    else:
        logger.info(
            f'''у пользователя в профиле заполнены
            first_name {message.from_user.first_name}
            и last_name: {message.from_user.last_name}''')
        await state.update_data(first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name)
        await message.answer('Для регистрации имя и фамилия указаны в профиле.')
        await message.answer('Введите ваш город:')
        await state.update_data(city=message.text)
        await state.set_state(Registration.birth_date)


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    logger.info(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name}
            отменил заполнение анкеты''')
    await message.answer(
        text='Чтобы снова перейти к заполнению анкеты - '
             'отправьте команду /start'
    )
    await state.clear()


@router.message(Registration.first_name, F.text.isalpha())
async def process_first_name(message: types.Message, state: FSMContext):
    logger.info(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name}
            заполняет first_name ''')
    await state.update_data(first_name=message.text)
    await message.answer('Введите ваше имя:')
    await state.set_state(Registration.last_name)


@router.message(Registration.last_name, F.text.isalpha())
async def process_first_name(message: types.Message, state: FSMContext):
    logger.info(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name}
            заполняет last_name ''')
    await state.update_data(last_name=message.text)
    await message.answer('Введите вашу фамилию:')
    await state.set_state(Registration.city)


@router.message(Registration.city)
async def process_last_name(message: types.Message, state: FSMContext):
    logger.info(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name}
            заполняет city
            стэйт: Registration.city''')
    await message.answer('Введите ваш город:')
    await state.update_data(city=message.text)
    await state.set_state(Registration.birth_date)


@router.message(Registration.birth_date)
async def process_city(message: types.Message, state: FSMContext):
    logger.info(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name}
            заполняет birth_date ''')
    await state.update_data(birth_date=message.text)
    await message.answer('Введите вашу дату рождения (например, 01.01.1990):')
    await state.set_state(Registration.email)


@router.message(Registration.email)
async def process_birth_date(message: types.Message, state: FSMContext):
    logger.info(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name}
            заполняет email ''')
    await state.update_data(email=message.text)
    await message.answer('Введите ваш email:')
    await state.set_state(Registration.end_update)


@router.message(Registration.end_update)
async def process_email(message: Message, state: FSMContext):
    data = await state.get_data()
    email = message.text

    user_id = message.from_user.id
    username = message.from_user.username or ''
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    city = data.get('city')
    birth_date = data.get('birth_date')

    # добавляем пользователя в базу
    add_user(user_id, username, first_name, last_name, city, birth_date, email)
    await message.answer('Вы успешно зарегистрированы!')
    # await state.finish()
    await state.clear()


@router.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
        logger.info(f'отправлено Эхо пользователю {message.from_user.id}')
    except TypeError:
        await message.reply(text='другой какой-то тип апдейтов')
