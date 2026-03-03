---
name: python-guidelines
description: >
  Python backend development guidelines based on the pylines project (community-of-python/pylines).
  Use this skill whenever writing, reviewing, or refactoring Python code — especially backend code
  with FastAPI, Litestar, SQLAlchemy, or similar stack. Trigger on any Python code generation,
  code review, architecture discussion, REST API design, test writing, or when the user mentions
  "pylines", "code style", "наши гайдлайны", "python guidelines", or asks to follow team conventions.
  Also trigger when writing pyproject.toml configs for ruff/mypy, designing class hierarchies,
  discussing SOLID in Python, or structuring a Python project.
---

# Python Guidelines (pylines)

Эти гайдлайны основаны на [community-of-python/pylines](https://github.com/community-of-python/pylines) — комплексном руководстве для Python backend/full-stack разработки.

При генерации или ревью Python кода **всегда** следуй правилам ниже. Если нужна детализация по конкретной теме, читай соответствующий reference-файл:

- `references/code-style.md` — стиль кода, типизация, именование, иммутабельность
- `references/rest.md` — REST API дизайн, URL conventions, версионирование
- `references/tests.md` — как писать тесты, AAA, параметризация, faker/hypothesis
- `references/solid.md` — SOLID принципы с примерами на Python
- `references/stack.md` — рекомендуемые библиотеки и инструменты

## Ключевые правила (всегда применять)

### Tooling
- Линтер и форматтер: **ruff** (select = ALL, с исключениями). Форматтер: **ruff format**
- Тайпчекер: **mypy --strict**
- Пакетный менеджер: **uv**
- Длина строки: **120 символов**
- Установка: `uv add --dev ruff mypy community-of-python-flake8-plugin flake8-pyproject auto-typing-final`

### Типизация
- 100% покрытие аннотациями типов — переменные, константы, атрибуты, аргументы
- Не аннотируй скалярные типы явно — mypy выведет сам (но `typing.Final` указывай)
- Сужай типы максимально: TypedDict лучше dict, Literal лучше str
- Все переменные аннотируй `typing.Final` (используй auto-typing-final для автоматизации)
- Все классы по умолчанию помечай `@typing.final`

### Именование
- Имена переменных и функций — минимум 8 символов. `a`, `b`, `data`, `user` — запрещены
- Функции называй **глаголами**: `fetch_user_balance`, `build_cache_key`, `process_payment`
- Не используй префикс `get` (кроме получения из оперативной памяти). Используй: fetch, retrieve, build, create, make, prepare, parse, download
- Используй конкретные имена с семантикой: `public_user` вместо `user`

### Классы
- Композиция вместо наследования. Не строй глубоких иерархий
- Базовый шаблон класса:
  ```python
  @dataclasses.dataclass(kw_only=True, slots=True, frozen=True)
  class HttpClient:
      httpx_connection: httpx.Client
      def fetch_user_balance(self, user_uuid: str) -> decimal.Decimal: ...
  ```
- Используй `typing.Protocol` для интерфейсов (статический этап, утиная типизация)

### Иммутабельность
- `typing.Final` на все переменные
- `@typing.final` на все классы
- `types.MappingProxyType` для словарей-констант
- `frozen=True` в dataclasses

### Исключения
- Никогда `except Exception` без крайней необходимости — ловить конкретный тип
- Сужай try-блок до минимума строк
- Предпочитай проверку перед действием (LBYL), а не перехват (EAFP): `if key in dict` вместо `except KeyError`
- Исключения — для исключительных ситуаций, не для нормального flow

### Импорты
- Встроенные библиотеки импортируй целиком: `import os`, `import typing`
- Если из модуля нужно >2 имён — импортируй модуль целиком

### Стиль
- Используй early return (инверсию условий) для уменьшения вложенности
- Не создавай временные переменные без причины
- Не пиши комментарии без необходимости — код должен быть самодокументируемым
- Регулярные выражения проверяй на ReDoS уязвимости

### Надёжность (Resilience)
- Всё, что выходит за оперативную память, может сломаться — используй retry
- Библиотека для retry: **stamina**
- Retry нужен для: SQL запросов, файловых операций, HTTP запросов, consumer/producer
- Ограничивай количество retry, рандомизируй интервал
- При высокой нагрузке — circuit breaker (circuit-breaker-box)

### REST API
- Формат: JSON, протокол: HTTP/2 или HTTP/3
- URL = ресурс (существительное), действие = HTTP метод
- Схема URL: `/rest/[сервис]/[сущность]/` для REST, `/rpc/[сервис]/[действие]/` для RPC
- Разделитель в URL: дефис (не подчёркивание)
- Вложенность запрещена: максимум `/[тип]/[сервис]/[сущность]/`
- Версионирование — через Accept заголовок, только если реально нужно
- Слеши в конце URL закрывай

### Тесты
- Паттерн AAA: Arrange → Act → Assert
- Предпочитай интеграционные тесты юнит-тестам
- Используй faker для генерации данных, hypothesis для property-based testing
- Параметризуй тесты через `@pytest.mark.parametrize`
- Всегда запускай параллельно: `pytest-xdist -n auto`

### Рекомендуемый стек
- Фреймворк: Litestar (основной), FastAPI (вторичный)
- ORM: SQLAlchemy
- DI: that-depends, modern-di, dishka
- Сервер: granian (не uvicorn)
- Логирование: structlog + MemoryHandler
- Валидация: pydantic или msgspec
- HTTP клиент: base-client (community-of-python), httpx для сложных случаев
- Конфигурация: pydantic-settings
- Фоновые задачи: taskiq
- Event-driven: faststream

### SOLID
- SRP: один класс = одна ответственность. Не инстанцируй зависимости внутри класса
- OCP: пиши обобщённый код. Если часто удаляешь старый код при добавлении нового — нарушение OCP
- LSP: покрывай код типами, mypy ловит большинство нарушений. Не бросай NotImplementedError в наследниках
- ISP: маленькие интерфейсы под конкретных потребителей, не раздувай Protocol
- DIP: используй DI паттерн + typing.Protocol. DI + утиная типизация = DIP

## pyproject.toml reference config

```toml
[tool.ruff]
fix = true
unsafe-fixes = true
line-length = 120

[tool.ruff.format]
docstring-code-format = true

[tool.ruff.lint]
select = ["ALL"]
external = ["COP"]
ignore = ["EM", "FBT", "TRY003", "D1", "D203", "D213", "G004", "FA", "COM812", "ISC001"]

[tool.ruff.lint.isort]
no-lines-before = ["standard-library", "local-folder"]
known-third-party = []
known-local-folder = []
lines-after-imports = 2

[tool.ruff.lint.extend-per-file-ignores]
"tests/*.py" = ["S101", "S311"]

[tool.mypy]
strict = true

[tool.flake8]
select = ["COP"]
exclude = [".venv", ".cache"]

[tool.coverage.report]
exclude_also = ["if typing.TYPE_CHECKING:"]
```
