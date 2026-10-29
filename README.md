# aiohttp-api

Учебный асинхронный REST API на aiohttp и клиент к нему: пользователи (добавить, получить, список), проверка входных данных схемами, документация API.

*English: a small async REST API on aiohttp with request validation (marshmallow) and Swagger docs, plus an async client example. Learning project.*

## Что внутри

- `server/` — приложение на aiohttp: маршруты `/add_user`, `/list_users`, `/get_user`; проверка запросов схемами marshmallow через `aiohttp-apispec`; единый обработчик ошибок в middleware (ответы в JSON); данные хранятся в памяти (`store/crm/accessor.py`).
- Документация API (Swagger): `/docs`, JSON-описание: `/docs/json`.
- `client/` — пример асинхронного клиента на `aiohttp.ClientSession` (с подробными комментариями про `await` и пул соединений).

## Как запустить

Нужен Python 3.10 (на нём делалось).

```bash
cd server
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Сервер запускается на `http://localhost:8080`, документация — `http://localhost:8080/docs`. Запускать нужно из каталога `server/`: конфигурация читается по относительному пути `app/config/config.yaml`.

## Стек

Python 3.10, aiohttp, aiohttp-apispec, marshmallow, asyncio, YAML.
