Функциональные требования:

1. Базовый функционал:
Бот должен получать текстовые сообщения и отправлять их обратно.
Все взаимодействия с ботом должны логироваться в консоли.


2. Сохранение пользователей:
При первом взаимодействии бот сохраняет ID, имя, фамилию, username пользователя в базу данных (например, SQLite или PostgreSQL).
Если пользователь уже есть в базе, бот просто отвечает сообщением без повторного сохранения.


3. Регистрация пользователей:
При первом использовании бот отправляет приветственное сообщение и предлагает зарегистрироваться.
Бот должен запросить у пользователя дополнительные данные:
    Полное имя (если его нет в профиле Telegram).
    Дату рождения.
    Город проживания.
    Email.

После ввода всех данных бот сохраняет их в БД.

*доки, которые использовал*
- aiogram       https://docs.aiogram.dev/en/stable/ 

- dataclasses   https://habr.com/ru/articles/415829/
- sqlite3       https://habr.com/ru/articles/754400/
                https://www.sqlite.org/doclist.html
                https://docs.python.org/3/library/sqlite3.html
- pip install py-asqlite3

- environs      https://pypi.org/project/environs/

- os.path       https://docs.python.org/3/library/os.path.html

- FSM           https://mastergroosha.github.io/aiogram-3-guide/fsm/

