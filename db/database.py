
from tortoise import Tortoise, fields
from tortoise.models import Model

from config import load_config, logger


DB_PATH = load_config().DB_PATH


class User(Model):
    user_id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=50)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    city = fields.CharField(max_length=50)
    birth_date = fields.CharField(max_length=10)
    email = fields.CharField(max_length=100)

    def __str__(self):
        return f'User {self.username}'


async def init_db():
    await Tortoise.init(
        db_url=f'sqlite://{DB_PATH}',
        modules={'models': ['db.database']}
    )
    await Tortoise.generate_schemas()
    logger.info('База данных создана')


async def user_exists(user_id):
    logger.info(f'Функция user_exists вызвана с user_id = {user_id}')
    return await User.filter(user_id=user_id).exists()


async def add_user(user_id, username, first_name, last_name, city, birth_date, email):
    logger.info(f'Добавляем пользователя {user_id} в базу данных')
    user, created = await User.get_or_create(
        user_id=user_id,
        defaults={
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "city": city,
            "birth_date": birth_date,
            "email": email
        }
    )
    if not created:
        await User.filter(user_id=user_id).update(
            username=username, first_name=first_name,
            last_name=last_name, city=city, birth_date=birth_date,
            email=email
        )
    logger.info(f'Пользователь {user_id} добавлен/обновлён')


async def get_user(user_id):
    logger.info(f'Получаем данные пользователя {user_id=}')
    user = await User.get_or_none(user_id=user_id)
    if user:
        return f'''Информация о пользователе {user.username}:
                Имя: {user.first_name}
                Фамилия: {user.last_name}
                Город: {user.city}
                Дата рождения: {user.birth_date}
                email: {user.email}
              '''
    else:
        return f'Пользователь с {user_id} не найден'
