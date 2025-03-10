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

- environs      https://pypi.org/project/environs/
                https://pythonrepo.com/repo/sloria-environs

- os.path       https://docs.python.org/3/library/os.path.html

- FSM           https://mastergroosha.github.io/aiogram-3-guide/fsm/

- tortoise      https://tortoise.github.io/#how-is-an-orm-useful
                https://habr.com/ru/articles/829222/
                https://pressanybutton.ru/post/tips-tricks/tortoise-orm-prostaya-asinhronnaya-alternativa-sql/

- pytest        https://docs.pytest.org/en/latest/how-to/xunit_setup.html