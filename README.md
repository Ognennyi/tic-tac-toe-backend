# Tic-Tac-Toe Backend

Backend для игры «Крестики-нолики», написанный на Python и Flask. Играть можно вдвоём или против компьютера.

## Возможности

- Регистрация пользователей и вход в систему.
- Создание игры с другим игроком или компьютером.
- Подключение к свободной игре.
- Проверка ходов, определение победителя и ничьей.
- Компьютерный противник с алгоритмом Minimax.
- Хранение пользователей и игр в PostgreSQL.

## Технологии

- Python, Flask — сервер и API.
- PostgreSQL, SQLAlchemy — база данных.
- Werkzeug — работа с паролями.
- Pytest — тестирование.

## Структура проекта

```text
src/
├── app.py          # Запуск сервера
├── web/            # Обработка HTTP-запросов
├── domain/         # Логика игры
├── datasource/     # Работа с базой данных
├── di/             # Создание и подключение сервисов
└── tests/          # Тесты
```

## Как запустить

Понадобятся **Python 3.10+** и **PostgreSQL**.

**1. Установить зависимости**

Из корневой папки проекта выполните:

```bash
python -m venv .venv
```

Активируйте окружение (Windows PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

На Linux/macOS используйте `source .venv/bin/activate`.

```bash
pip install -r requirements.txt
```

**2. Настроить базу данных**

В PostgreSQL создайте базу с именем `tic_tac_toe`:

```sql
CREATE DATABASE tic_tac_toe;
```

Создайте в корне проекта файл `.env` по образцу `.env.example` и укажите пароль пользователя PostgreSQL `postgres`:

```env
DB_PASSWORD=ваш_пароль
```

В коде используется подключение к PostgreSQL на `localhost:5432` от имени `postgres`.

**3. Создать таблицы и запустить сервер**

Из корня проекта:

```bash
cd src
python -c "from datasource.database import Base, engine; import datasource.model.user, datasource.model.game; Base.metadata.create_all(bind=engine)"
python app.py
```

Сервер запустится на `http://127.0.0.1:5000`.

## Основные запросы API

| Метод | Адрес | Действие |
| --- | --- | --- |
| `POST` | `/auth/signup` | Регистрация |
| `POST` | `/auth/login` | Вход |
| `GET` | `/users/<user_id>` | Получение пользователя |
| `POST` | `/game` | Создание игры |
| `GET` | `/games/available` | Список свободных игр |
| `POST` | `/games/<game_id>/join` | Подключение к игре |
| `GET` | `/game/<game_id>` | Информация об игре |
| `POST` | `/game/<game_id>` | Сделать ход |

Пример данных для регистрации (`POST /auth/signup`):

```json
{
  "login": "player1",
  "password": "123456"
}
```

Для входа и остальных запросов используется **HTTP Basic Auth** (логин и пароль). Вход возвращает `user_id`, а не токен.

## Тесты

Из папки `src`:

```bash
python -m pytest tests
```

Часть тестов использует PostgreSQL, поэтому база должна быть настроена заранее.

> Проект предназначен для локального запуска и учебных целей. В `app.py` включён режим отладки Flask.
