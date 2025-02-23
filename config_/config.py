from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str         # Название базы данных
    db_host: str          # URL-адрес базы данных
    db_user: str          # Username пользователя базы данных
    db_password: str      # Пароль к базе данных


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admin_ids=list(map(int, env.list('ADMIN_IDS')))))


'''
config = Config(
    tg_bot=TgBot(token=BOT_TOKEN, admin_ids=ADMIN_IDS),
    db=DatabaseConfig(
        db_host=DB_HOST,
        db_user=DB_USER,
        db_password=DB_PASSWORD,
        database=DATABASE
    )
)
'''

'''
Или ещё тупее, если будем из мэйна делать импорт:
from config import BOT_TOKEN
bot: Bot = Bot(BOT_TOKEN)

а в конфиг тогда вписать что-то такое:
BOT_TOKEN: str = 356345345:1234567qwe1234567
'''
