import os
import pytest
from config import load_config, Config


@pytest.fixture
def temp_env():
    '''Фикстура для временного изменения переменных окружения'''
    old_env = os.environ.copy()
    os.environ.update({
        'BOT_TOKEN': 'test_bot_token',
        'DB_PATH': 'test_db.sqlite',
        'EMAIL_REGEX': r'^[\w\.-]+@[\w\.-]+\.\w+$'
    })
    yield
    os.environ.clear()
    os.environ.update(old_env)


def test_load_config(temp_env):
    '''Тестируем загрузку конфигурации'''
    config = load_config()

    assert isinstance(config, Config)
    assert config.BOT_TOKEN == 'test_bot_token'
    assert config.DB_PATH == 'test_db.sqlite'
    assert config.EMAIL_REGEX == r'^[\w\.-]+@[\w\.-]+\.\w+$'


# pytest -v -s
# pytest --maxfail=2
# pytest -k "config"
# pytest --tb=short   сокращенный трэйсбэк
# pytest --cov=config
# pytest --cov=config
