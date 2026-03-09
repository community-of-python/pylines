# Code Style — полное руководство

Источник: community-of-python/pylines/code-style.md

## Настройка

```bash
uv add --dev ruff mypy community-of-python-flake8-plugin flake8-pyproject auto-typing-final
```

Добавь конфиг в pyproject.toml (см. SKILL.md).

### Почему отключены конкретные правила ruff

Включай ALL, затем исключай:
- **EM** — заводить отдельную переменную для строки в Exception не обязательно
- **FBT** — boolean аргументы допустимы
- **TRY003** — писать message в exception нормально
- **S101** — assert опасны, но в тестах повсеместны (отключаем только для tests/)
- **D1, D203, D213** — принуждать к докстрингам без разбора → «капитан очевидность»
- **FA** — не поддерживаем старые версии Python
- **COM812, ISC001** — несовместимы с ruff format

## Типизация

100% покрытие аннотациями. mypy strict. Не пиши скалярные типы — mypy выведет:

```python
# ❌
some_var: str = 'something'
another_var: int = 5

# ✅
some_var = 'something'
another_var = 5
```

Сужай типы максимально:
```python
# ❌
SOME_CONST: dict = {'what': 5, 'kek': 'raz'}

# ✅ TypedDict
class SomeConstDict(typing.TypedDict):
    what: int
    kek: str

SOME_CONST: typing.Final[SomeConstDict] = {'what': 5, 'kek': 'raz'}
```

## Именование

- Минимум 8 символов для имён переменных и функций
- Функции = глаголы: fetch_, build_, create_, make_, prepare_, parse_, download_
- Не используй get_ (кроме чтения из RAM). Используй конкретные глаголы
- Имена с семантикой: `public_user` вместо `user`, `payment_response` вместо `data`

```python
# ❌
class HttpFetcher:
    def get_http_result(self): ...

# ✅
class HttpFetcher:
    def fetch_http_result(self): ...

# ❌
class SomethingWithCache:
    def get_cache_key(self, user_id): ...

# ✅
class SomethingWithCache:
    def build_cache_key(self, user_id): ...
```

## Иммутабельность

```python
import types
import typing

# typing.Final на все переменные
some_cool_var: typing.Final = 10

def do_something(hello: str) -> None:
    hello_guys: typing.Final = f'{hello}{some_cool_var}'
    print(hello_guys)

# MappingProxyType для словарей
SOME_CONST: typing.Final = types.MappingProxyType({'key': 'value'})
```

- auto-typing-final автоматизирует расстановку Final
- @typing.final на все классы по умолчанию

## Классы

```python
@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)
class HttpClient:
    httpx_connection: httpx.Client

    def fetch_user_balance_from_crm(self, user_uuid: str) -> decimal.Decimal:
        ...
```

- frozen = иммутабельность
- slots = экономия памяти
- kw_only = только именованные аргументы (меньше ошибок)
- Композиция вместо наследования

## Исключения

- Конкретный тип вместо `except Exception`
- Минимум строк в try-блоке
- LBYL > EAFP: проверяй перед действием (`if key in dict` вместо `except KeyError`)
- Исключения — для исключительных случаев, не для нормального flow
- Иерархия: LookupError → IndexError, KeyError
- dict.get() возвращает None вместо падения

## Early return

```python
# ❌ Глубокая вложенность
def process(payload):
    if payload:
        if isinstance(payload, list):
            if all(isinstance(i, int) for i in payload):
                ...

# ✅ Инверсия
def process(payload):
    if not payload:
        return
    if not isinstance(payload, list):
        return
    ...
```

## Прочее

- Не создавай временные переменные без причины
- Не пиши комментарии без необходимости
- Регулярки проверяй на ReDoS: https://devina.io/redos-checker
- Избегай магии: hasattr, getattr — признаки неявного поведения
- Зен Питона — афоризмы, не правила. Цитировать бесполезно, используй конкретные правила
