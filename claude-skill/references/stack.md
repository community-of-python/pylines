# Recommended Stack

Источник: community-of-python/pylines/our-stack.md

## Фреймворки
- **Litestar** (основной), **FastAPI** (вторичный)
- MPA/админки: **Django** (+ django-ninja для REST)
- Бойлерплейтинг: **microbootstrap**

## Сервер
- **granian** (вместо uvicorn)

## DI
- **that-depends**, **modern-di**, **dishka**

## ORM / БД
- **SQLAlchemy**
- NoSQL: **Redis/Valkey/Dragonfly** через **redis-py** (async)

## HTTP клиенты
- **base-client** (community-of-python) — типизированный, с retry и circuit breaker
- **httpx** / **niquests** — для сложных случаев
- **curl_cffi** — если блокируют парсинг

## Валидация
- **pydantic** или **msgspec**

## Конфигурация
- **pydantic-settings**

## Тестирование
- **pytest**, **pytest-xdist**, **hypothesis**, **schemathesis**, **polyfactory**, **faker**

## Event-driven
- **faststream** (+ transactional outbox/inbox)

## Фоновые задачи
- **taskiq**

## Retry / Resilience
- **stamina** (retry)
- **circuit-breaker-box** (circuit breaker)

## Логирование
- **structlog** + **MemoryHandler**

## Observability
- **OpenTelemetry** (+ zero-code instrumentation)

## Линтеры
- **ruff** (lint + format), **mypy** (strict)

## Пакетный менеджер
- **uv**

## Кеширование
- **cachebox**

## CLI
- **typer**

## Файловые операции
- Sync: **pathlib** (не os.path)
- Async: **aiofile** (не aiofiles)

## Прочее
- Даты: **pendulum**
- Изображения: **pyvips**
- Multiprocessing: **mpire**
- Async boilerplate: **aiorun**
- Секреты: **secrets** (stdlib)
- AI/LLM: **pydantic-ai**
- MCP: **fastmcp**
- HTML parsing: **selectolax**
- File type detection: **python-magic** + **magika**
- Auth: **Keycloak** + **Apisix** + **Istio** (mTLS)
- Performance: **PyPy** или **pyston**
