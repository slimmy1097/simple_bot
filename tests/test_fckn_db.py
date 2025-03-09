import pytest
import asyncio
from tortoise import Tortoise
from ..db.db_work import User, init_main, add_user, user_exists, get_user, DB_PATH


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def initialize_db():
    await Tortoise.init(
        db_url=f'sqlite://{DB_PATH}',
        modules={'models': ['your_module']}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_add_user(initialize_db):
    await add_user(1, 'testuser', 'Test', 'User', 'TestCity', '2000-01-01', 'test@example.com')
    user = await User.get_or_none(id=1)
    assert user is not None
    assert user.username == 'testuser'


@pytest.mark.asyncio
async def test_user_exists(initialize_db):
    await add_user(2, 'anotheruser', 'Another', 'User', 'AnotherCity', '1990-12-12', 'another@example.com')
    exists = await user_exists(2)
    assert exists is not None


@pytest.mark.asyncio
async def test_user_does_not_exist(initialize_db):
    exists = await user_exists(999)
    assert exists is None


@pytest.mark.asyncio
async def test_get_user(initialize_db):
    await add_user(3, 'getuser', 'Get', 'User', 'GetCity', '1980-11-11', 'get@example.com')
    user_info = await get_user(3)
    assert 'Get' in user_info
    assert 'User' in user_info
    assert 'GetCity' in user_info


@pytest.mark.asyncio
async def test_update_user(initialize_db):
    await add_user(4, 'olduser', 'Old', 'User', 'OldCity', '1970-10-10', 'old@example.com')
    await add_user(4, 'newuser', 'New', 'User', 'NewCity', '1970-10-10', 'new@example.com')
    user = await User.get_or_none(id=4)
    assert user.username == 'newuser'
    assert user.city == 'NewCity'


@pytest.mark.asyncio
async def test_add_multiple_users(initialize_db):
    await add_user(5, 'user5', 'Five', 'User', 'City5', '2005-05-05', 'five@example.com')
    await add_user(6, 'user6', 'Six', 'User', 'City6', '2006-06-06', 'six@example.com')
    user5 = await User.get_or_none(id=5)
    user6 = await User.get_or_none(id=6)
    assert user5 is not None
    assert user6 is not None


@pytest.mark.asyncio
async def test_get_nonexistent_user(initialize_db):
    user_info = await get_user(999)
    assert 'не найден' in user_info


@pytest.mark.asyncio
async def test_user_fields(initialize_db):
    await add_user(7, 'user7', 'Seven', 'User', 'City7', '2007-07-07', 'seven@example.com')
    user = await User.get_or_none(id=7)
    assert user.email == 'seven@example.com'
    assert user.birth_date == '2007-07-07'


@pytest.mark.asyncio
async def test_database_initialization(initialize_db):
    user = await User.get_or_none(id=1)
    assert user is not None


@pytest.mark.asyncio
async def test_user_deletion(initialize_db):
    await add_user(8, 'user8', 'Eight', 'User', 'City8', '2008-08-08', 'eight@example.com')
    user = await User.get_or_none(id=8)
    assert user is not None
    await user.delete()
    user = await User.get_or_none(id=8)
    assert user is None
