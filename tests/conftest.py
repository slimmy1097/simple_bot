import sys
import os

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


# Явно добавить корневую директорию в sys.path
# pytest должен подхватить этот файл при запуске тестов
# потому что тетсы в папке с тестами и они не могут подхватить конфиг, который директорией выше

# еще вариант запуска:
# PYTHONPATH=. pytest tests/
