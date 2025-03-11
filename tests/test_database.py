import pytest
import pytest_asyncio
from tortoise import Tortoise
from db.db_work import init_main, add_user, user_exists, get_user
from db.db_work import User  # Импорт модели


# тестовая БД (sqlite в памяти)
TEST_DB_URL = 'sqlite://:memory:'


@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_test_db():
    '''Фикстура для инициализации тестовой базы перед каждым тестом'''
    await Tortoise.init(
        db_url=TEST_DB_URL,
        modules={'models': ['db.db_work']}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()  # Закрываем соединение после тестов


@pytest.mark.asyncio
async def test_add_user():
    '''Тестируем добавление пользователя.'''
    await add_user(
        user_id=1111,
        username='testuser',
        first_name='Test',
        last_name='User',
        city='TestCity',
        birth_date='2000-01-01',
        email='test@mail.ru'
    )

    user = await User.get(id=1111)
    assert user is not None
    assert user.username == 'testuser'
    assert user.email == 'test@mail.ru'


@pytest.mark.asyncio
async def test_user_exists():
    '''проверка существования пользователя'''
    await add_user(
        user_id=2222,
        username='another_test_user',
        first_name='another_name',
        last_name='another_fami',
        city='another_city',
        birth_date='1999-11-11',
        email='another_test@mmmmmmmail.com'
    )

    user = await user_exists(2222)
    assert user is not None
    assert user.username == 'another_test_user'

    '''проверка НЕсуществования пользователя'''
    user_not_found = await user_exists(999)
    assert user_not_found is None


@pytest.mark.asyncio
async def test_get_user():
    '''Тестируем получение информации о пользователе.'''
    await add_user(
        user_id=3333,
        username='info_user',
        first_name='info_first',
        last_name='info_last',
        city='info_city',
        birth_date='1984-01-01',
        email='info@ggggggg.com'
    )

    result = await get_user(3333)
    assert 'Информация о пользователе info_user' in result
    assert 'Имя: info_first' in result
    assert 'Фамилия: info_last' in result
    assert 'Город: info_city' in result

    result_not_found = await get_user(999)
    assert result_not_found == 'Пользователь с 999 не найден'
