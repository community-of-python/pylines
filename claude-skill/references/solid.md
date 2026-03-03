# SOLID Guide

Источник: community-of-python/pylines/solid.md

## Общие соглашения

- SOLID — про ООП, применяй осознанно
- Покрывай код 100% аннотациями типов + mypy strict
- Интерфейс = typing.Protocol (статический этап, утиная типизация)
- Трактовка из оригинала: Agile Software Patterns, Principles and Development (2003)

## SRP — Single Responsibility Principle

> Класс должен иметь одну причину для изменений

- «Причина» — командная договорённость, определяйте эмпирически
- Не инстанцируй зависимости внутри класса — передавай снаружи

```python
# ❌ Нарушает SRP: содержит подключения к kafka, postgres
@dataclasses.dataclass
class UserService:
    database_host: str
    kafka_host: str
    async def create_user(self, user_data): ...  # создаёт соединения внутри

# ✅ Зависимости передаются извне
@dataclasses.dataclass
class UserService:
    database_connection: asyncpg.Connection
    kafka_producer: aiokafka.AIOKafkaProducer
    async def create_user(self, user_data): ...
```

## OCP — Open/Closed Principle

> Открыт для расширения, закрыт для модификации

- Пиши обобщённый код, чтобы добавлять новое без переписывания старого
- Индикаторы нарушения: цепочки if/elif, частое удаление кода в PR

```python
# ❌ Каждая новая команда — правка функции
def run_command(name, **opts):
    if name == "list-pods": return list_pods(**opts)
    elif name == "scale": return scale(**opts)

# ✅ Маппинг
AVAILABLE_COMMANDS = {"list-pods": list_pods, "scale": scale}
def run_command(name, **opts):
    if handler := AVAILABLE_COMMANDS.get(name):
        return handler(**opts)
```

## LSP — Liskov Substitution Principle

> Подклассы должны заменять базовые классы без нарушения работы

- Покрывай типами — mypy ловит большинство нарушений
- Не бросай NotImplementedError в наследниках

```python
# ❌ Penguin.fly() бросает NotImplementedError
class Bird:
    def fly(self): ...
class Penguin(Bird):
    def fly(self): raise NotImplementedError

# ✅ Разделяй иерархию
class GenericBird: ...
class FlyingBird(GenericBird):
    def fly(self): ...
class Penguin(GenericBird): ...
```

## ISP — Interface Segregation Principle

> Клиенты не должны зависеть от методов, которыми не пользуются

- Маленькие Protocol под конкретных потребителей
- Не раздувай интерфейс «про запас»

## DIP — Dependency Inversion Principle

> Зависимости на абстракции, не на конкретные реализации

- DI паттерн + typing.Protocol = DIP в Python
- DI контейнеры: that-depends, modern-di, dishka

```python
class Notifier(typing.Protocol):
    def notify(self, message: str) -> None: ...

class OrderProcessor:
    def __init__(self, notifier: Notifier) -> None:
        self.notifier = notifier
```
