import re

from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup

from db.db_work import user_exists, add_user, get_user

from config import load_config, logger
from datetime import datetime


router = Router()
EMAIL_REGEX = load_config().EMAIL_REGEX


# функкции проверки даты и email
def ok_date(date_string: str) -> bool:
    try:
        birth_date = datetime.strptime(date_string, '%d.%m.%Y')
        today = datetime.today()
        age = (today - birth_date).days // 365

        # просто для логов
        formatted_today = today.strftime('%d.%m.%Y')

        logger.info(f'''Пользователь вводит {birth_date}
                                Сегодня: {formatted_today}
                                Возраст: {age} лет''')
        return 5 <= age <= 120
    except ValueError:
        return False


def ok_email(email_string: str) -> bool:
    return bool(re.match(EMAIL_REGEX, email_string))


class Registration(StatesGroup):
    first_name = State()
    last_name = State()
    city = State()
    birth_date = State()
    email = State()
    end_update = State()


# Первая часть стэйтов, которые срабатывают если пользователь в default_state
# и если не выбрал команду старт. Пользщователь есть - отправляют эхо.
# нет пользователя - первое приветственное сообщение, 1 раз


# посмотреть свои статы

@router.message(StateFilter(default_state), Command('selfinfo'))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    response_from_db = await get_user(user_id)
    logger.info(
        f'выбрана команда /selfinfo, получение инфо о себе \n{user_id=}\n{response_from_db}\n')
    await message.answer(response_from_db)


@router.message(StateFilter(default_state), ~Command('start'))
async def first_enter(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or ''

    logger.debug(
        f'Самый первый хэндлер default_state, реагирует на любые команды кроме /start')
    if not await user_exists(user_id):
        await message.answer(
            'Привет!\n\nДавай зарегистрируем тебя\nДля регистрации /start')
    else:
        try:
            await message.send_copy(chat_id=message.chat.id)
            logger.info(f'Отправлено Эхо пользователю {message.from_user.id}')
        except TypeError:
            await message.reply(text='другой какой-то тип апдейтов')


# Вторая часть стэйтов, на всё остальное, кроме отмена регистрации
# Первый из них - default_state и команда start

@router.message(StateFilter(default_state), Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or ''

    logger.info('выбрана команда /start, выполняется cmd_start')

    if not message.from_user.first_name or not message.from_user.last_name:
        logger.debug(
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
        await message.answer('Для регистрации имя и фамилия указаны в профиле.\nВведите ваш город:')
        # await state.update_data(city=message.text)
        await state.set_state(Registration.city)


@router.message(Registration.first_name, F.text.isalpha())
async def process_first_name(message: types.Message, state: FSMContext):
    logger.debug(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name}
            заполняет first_name ''')
    await state.update_data(first_name=message.text)
    await message.answer('Введите вашу фамилию:')
    await state.set_state(Registration.last_name)


@router.message(Registration.first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    logger.debug(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name}
            некорректно заполнил имя''')
    await message.answer('Имя было введено некорректно. Повторите:')


@router.message(Registration.last_name, F.text.isalpha())
async def process_last_name(message: types.Message, state: FSMContext):
    logger.info(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name}
            заполняет last_name ''')
    await state.update_data(last_name=message.text)
    await message.answer('Введите ваш город:')
    await state.set_state(Registration.city)


@router.message(Registration.last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    logger.info(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name}
            некорректно ввел фамилию''')
    await message.answer('Фамилия была введена некорректно. Повторите:')


# обрабытываем город

@router.message(Registration.city, F.text.isalpha())
async def process_city(message: types.Message, state: FSMContext):
    logger.info(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name} заполняет city\n''')
    await message.answer('Введите дату рождения (например, 01.01.1990):')
    await state.update_data(city=message.text)
    await state.set_state(Registration.birth_date)


@router.message(Registration.city)
async def process_city(message: types.Message, state: FSMContext):
    logger.info(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name}
            некорректно ввел город\n''')
    await message.answer('Город введен некорректно. Повторите:')


# обрабытываем дату рождения

@router.message(Registration.birth_date, lambda message: ok_date(message.text))
async def process_birth_date(message: types.Message, state: FSMContext):
    logger.info(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name}
            заполняет birth_date ''')
    await state.update_data(birth_date=message.text)
    await message.answer('Введите ваш email:')
    await state.set_state(Registration.email)


@router.message(Registration.birth_date)
async def process_birth_date(message: types.Message, state: FSMContext):
    logger.info(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name}
            некорректно ввел дату рождения''')
    await message.answer('Некорректно введена дата рождения. Повторите:')


# обрабытываем дату email

@router.message(Registration.email, lambda message: ok_email(message.text))
async def process_email(message: types.Message, state: FSMContext):
    logger.info(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name} ввел email ''')
    await state.update_data(email=message.text)
    await message.answer('Записываем данные')
    await state.set_state(Registration.end_update)
    await process_end_update(message, state)


@router.message(Registration.email)
async def process_email(message: types.Message, state: FSMContext):
    logger.info(
        f'''пользователь {message.from_user.first_name} {message.from_user.last_name}
            некорректно ввел email ''')
    await message.answer('Некорректно введен email:')


@router.message(Registration.end_update)
async def process_end_update(message: Message, state: FSMContext):
    data = await state.get_data()

    user_id = message.from_user.id
    username = message.from_user.username or ''
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    city = data.get('city')
    birth_date = data.get('birth_date')
    email = data.get('email')

    # добавляем пользователя в базу
    await add_user(user_id, username, first_name, last_name, city, birth_date, email)
    await message.answer('Вы успешно зарегистрированы!')
    await state.clear()


# cancel , работает только если пользователь в процессе регистрации

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
