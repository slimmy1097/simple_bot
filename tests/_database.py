import pytest
from tortoise import Tortoise
from db.database import init_db, User, user_exists, add_user, get_user


@pytest.fixture(scope="function", autouse=True)
async def setup_test_db():
    """
    Фикстура, создающая тестовую БД в памяти перед каждым тестом и удаляющая её после.
    """
    await Tortoise.init(
        db_url="sqlite://:memory:",  # Используем временную SQLite БД в памяти
        modules={"models": ["db.database"]}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_init_db():
    """Проверяем, создаётся ли база данных без ошибок."""
    await init_db()
    assert await User.all() == []  # БД пуста после инициализации


@pytest.mark.asyncio
async def test_user_exists():
    """Проверяем, что user_exists() правильно определяет наличие пользователя."""
    user_id = 123
    assert not await user_exists(user_id)  # Пользователь ещё не создан

    await User.create(user_id=user_id, username="testuser",
                      first_name="Test", last_name="User", city="TestCity",
                      birth_date="2000-01-01", email="test@example.com")

    assert await user_exists(user_id)  # Теперь пользователь существует


@pytest.mark.asyncio
async def test_add_user():
    """Проверяем, что пользователь создаётся и обновляется корректно."""
    user_id = 456
    await add_user(user_id, "newuser", "New", "User", "NewCity", "1999-12-31", "new@example.com")

    user = await User.get(user_id=user_id)
    assert user.username == "newuser"
    assert user.city == "NewCity"

    # Обновим пользователя
    await add_user(user_id, "updateduser", "Updated", "User", "UpdatedCity", "1999-12-31", "updated@example.com")

    user = await User.get(user_id=user_id)
    assert user.username == "updateduser"
    assert user.city == "UpdatedCity"


@pytest.mark.asyncio
async def test_get_user():
    """Проверяем корректность вывода get_user()."""
    user_id = 789
    await User.create(user_id=user_id, username="testname",
                      first_name="Test", last_name="Surname", city="TestCity",
                      birth_date="1990-05-05", email="test@email.com")

    result = await get_user(user_id)
    assert "Информация о пользователе testname" in result
    assert "Имя: Test" in result
    assert "Город: TestCity" in result

    # Проверим случай, когда пользователя нет
    result = await get_user(999)
    assert "Пользователь с 999 не найден" in result
