from tortoise import Tortoise, fields, models, run_async
from config import load_config, logger

DB_PATH = load_config().DB_PATH


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    city = fields.CharField(max_length=50)
    birth_date = fields.CharField(max_length=16)
    email = fields.CharField(max_length=100)

    class Meta:
        table = 'users'     # имя таблицы


async def init_main():
    await Tortoise.init(
        db_url=f'sqlite://{DB_PATH}',
        modules={'models': ['db.db_work']}
    )
    await Tortoise.generate_schemas()   # создание таблицы, если её (их) нет
    logger.info('База данных готова')


async def add_user(user_id, username, first_name, last_name, city, birth_date, email):
    # Возвращает tuple, в котором на первом индексе сам объект,
    # а на втором булевый флаг, показывающий, был ли создан объект.
    user, created = await User.update_or_create(
        id=user_id,
        defaults={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'city': city,
            'birth_date': birth_date,
            'email': email,
        }
    )
    if created:
        logger.info(
            f'добавляем / обновляем пользователя {user_id=} в БД {created=}')
    else:
        logger.info(
            f'обновляем пользователя {user_id=} в БД')


async def user_exists(user_id):
    logger.info(f'Функция user_exists вызвана с {user_id=}')
    # get_or_none - чтобы не писать try \ except
    user = await User.get_or_none(id=user_id)
    return user


async def get_user(user_id):
    logger.info(f'Получаем данные пользователя {user_id=}')
    user = await User.filter(id=user_id).first()
    if user:
        print('not null, okey')
        print(user.username)
        return f'''Информация о пользователе {user.username}:
                Имя: {user.first_name}
                Фамилия: {user.last_name}
                Город: {user.city}
                Дата рождения: {user.birth_date}
                email: {user.email}
              '''
    else:
        return f'Пользователь с {user_id} не найден'


# Для тестов на ходу, для проверки кода
async def main():
    await init_main()
    await add_user(123456, 'test_username', 'test_first_name', 'test_last_name',
                   'test_city', 'test_birth_date', 'test_email')
    print(await user_exists(12345))
    print(await user_exists(111))

    await get_user(123456)
    print(await get_user(123456))
    await get_user(173831742)

if __name__ == '__main__':
    run_async(main())
