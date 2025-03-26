Recommended solutions
===
Здесь список библиотек и фреймворков, инфраструктурных решений и справочников, которые мы выбираем:

1. Наши фреймворки это [FastAPI](https://github.com/tiangolo/fastapi) и [Litestar](https://github.com/litestar-org/litestar)
1. Для базового бойлерплейтинга сервисов используем [microbootstrap](https://github.com/community-of-python/microbootstrap)
1. Наш логгер это [structlog](https://www.structlog.org/en/stable/)
1. Python application сервер это [granian](https://github.com/emmett-framework/granian) (вместо uvicorn)
1. DI фреймворки: [that depends](https://github.com/modern-python/that-depends), [modern di](https://github.com/modern-python/modern-di/) или [dishka](https://github.com/reagento/dishka)
1. ORM: sqlalchemy
1. Наш набор для тестирования: pytest, [pytest-xdist](https://github.com/pytest-dev/pytest-xdist), [hypothesis](https://github.com/HypothesisWorks/hypothesis), [schemathesis](https://github.com/schemathesis/schemathesis), [polyfactory](https://polyfactory.litestar.dev/latest/), faker
1. Event driven architecture: [faststream](https://github.com/airtai/faststream) (совместите с transactional outbox/inbox для большей надежности)
1. Настройки: [pydantic settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
1. HTTP клиенты: [httpx](https://www.python-httpx.org/) или [niquests](https://niquests.readthedocs.io/en/latest/)
1. Для работы с файлами используем [aiofile](https://github.com/mosquito/aiofile)
1. Метрики, observability — [open telemetry](https://opentelemetry.io/docs/languages/python/), для некоторых сервисов вы можете [использовать автоматическую/zerocode интроспекцию](https://opentelemetry.io/docs/zero-code/python/)
1. Для background задач мы используем [taskiq](https://github.com/taskiq-python/taskiq)
1. Наш линтер и форматтер это ruff (check, format, fix режимы вам все полезны), а так же mypy (мы много испольузуем библиотеку [typing](https://docs.python.org/3/library/typing.html))
1. Наша noSQL база это [valkey](https://valkey.io/) или [dragonfly](https://www.dragonflydb.io/); для доступа к ним используем асинхронный [Redis py](https://github.com/redis/redis-py)
1. Наш пакетный менеджер это uv (+ управление версиями питона)
1. Для аутентификации имеет смысл брать keycloack, для авторизации apisix + keycloack, межсервисную аутентификацию имеет смысл строить на mTLS (apisix + istio)
1. Для ускорения питона имеет можно брать pypy
1. [CNCF landscape](https://landscape.cncf.io/) — энциклопедия devops решений
1. [Microservices.io](https://microservices.io/) и [system design primer](https://github.com/donnemartin/system-design-primer) — справочники по микросервисам
