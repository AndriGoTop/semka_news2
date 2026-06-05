# SemkaNews - новости для чётких ребят

## Quick start
### Пример файла .env, который должен находиться в корневой папке проекта
```dotenv
POSTGRES_PASSWORD=<Пароль БД>
POSTGRES_USER=<Пользователь БД>
POSTGRES_DB=<Имя БД>
POSTGRES_HOST=<Адрес БД (Если поднимать через Docker compost, то значение -- bd)>
POSTGRES_PORT=5432
GIGA_KEY=<API ключ GigaChat>
GIGA_USER_ID=<ID пользователя GigaChat>
```
### Команда для того, чтобы поднять проект
```commandline
docker compose up -d
```