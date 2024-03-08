Язык: Python 3.11  
Фреймворк: FastAPI 0.110.0  
База данных: Postgresql 16  
ORM: Sqlalchemy 2.0.28 + asyncpg (драйвер)  

## Запуск 
### docker-compose
Для запуска приложения можно воспользоваться готовым докер образом, и готовым **docker-compose.yml** файлом.
```bash
docker-compose build && docker-compose up
```
Приложение будет запущено локально на порту 7000 (можно поменять в файле **docker-compose.yml**,
в разделе *services>python>ports*) вместе с тестовой бд.

### Отдельно

Для запуска отдельно приложения нужно установить переменные окружения как в файле
**.env**. 

**Самыми главными являются переменные**

DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME отвечающие за подключение
к бд.

JWT_SECRET - ключ для шифрования jwt-токенов
JWT_ALGORITHM - алгоритм шифрования jwt-токенов

**Переменные которым можно оставить стандартное значение:**

REFRESH_TOKEN_COOKIE_NAME - название куки в которой будет лежать refresh-токен

REFRESH_TOKEN_DURATION_DAYS - период действия refresh-токена в днях

ACCESS_TOKEN_COOKIE_NAME - название куки в которой будет лежать access-токен

ACCESS_TOKEN_DURATION_MINUTES - период действия access-токена в минутах

**Необязательные переменные**

TELEGRAM_BOT_TOKEN - токен для бота в Telegram

TELEGRAM_CHAT_ID - id чата, в который бот будет присылать сообщения о критических ошибках

**Непосредственно запуск**

Установить пакеты с помощью poetry
```bash
poetry config virtualenvs.create false && poetry install --without dev
```
И запустить (из корневой папки) указав порт
```bash
uvicorn src.app:app --port {port}
```

### API

При работе с API нужно сначала зарегистрировать нового пользователя
или войти с помощью существующего. Т.к. access-токен действует только 30 минут (можно изменить см. выше)
то периодически будет выскакивать ошибка 401, Not authenticated. При
её возникновении следует обратиться к маршруту /api/auth/refresh_tokens.
Он обновит токен и можно будет работать дальше.