 # Recommended solutions

This is a list of libraries, frameworks, infrastructure solutions, and references we choose:

1. Our frameworks: [Litestar](https://github.com/litestar-org/litestar) (main, prefferred) and [FastAPI](https://github.com/tiangolo/fastapi) (secondary)
1. For MPA projects and admin panels: [django](https://github.com/django/django). Also maybe paired with [django-ninja](https://github.com/vitalik/django-ninja) for REST
1. For basic service boilerplating is a must: [microbootstrap](https://github.com/community-of-python/microbootstrap)
1. Python application server: [granian](https://github.com/emmett-framework/granian) (instead of [Uvicorn](https://github.com/encode/uvicorn))
1. DI frameworks: [that depends](https://github.com/modern-python/that-depends), [modern di](https://github.com/modern-python/modern-di/), or [dishka](https://github.com/reagento/dishka)
1. ORM: [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy)
1. Our testing suite: [pytest](https://github.com/pytest-dev/pytest), [pytest-xdist](https://github.com/pytest-dev/pytest-xdist), [hypothesis](https://github.com/HypothesisWorks/hypothesis), [schemathesis](https://github.com/schemathesis/schemathesis), [polyfactory](https://polyfactory.litestar.dev/), [faker](https://github.com/joke2k/faker)
1. Event-driven architecture: [faststream](https://github.com/airtai/faststream) (combine with transactional outbox/inbox for greater reliability)
1. For retries: [stamina](https://github.com/hynek/stamina)
1. Configuration management: [pydantic settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
1. HTTP clients: [httpx](https://www.python-httpx.org/) or [niquests](https://niquests.readthedocs.io/en/latest/) (in wich streaming is broken, be careful)
1. File operations:
   1. Sync: [pathlib](https://docs.python.org/3/library/pathlib.html). Not recommended: os.path
   1. Async: [aiofile](https://github.com/mosquito/aiofile). Not recommended: aiofile**s**
1. Secrets generation: [secrets](https://docs.python.org/3/library/secrets.html)
1. Metrics and observability: [open telemetry](https://opentelemetry.io/docs/languages/python/), for some services you can [use automatic/zero-code instrumentation](https://opentelemetry.io/docs/zero-code/python/)
1. For background tasks: [taskiq](https://github.com/taskiq-python/taskiq)
1. Linters and formatters: [ruff](https://github.com/astral-sh/ruff) (check, format, fix modes are all useful) and [mypy](https://github.com/python/mypy) (we heavily use the [typing](https://docs.python.org/3/library/typing.html) library)
1. Our NoSQL databases: [redis](https://github.com/redis/redis), or [valkey](https://valkey.io/)/[dragonfly](https://www.dragonflydb.io/); for accessing them, we use asynchronous [Redis py](https://github.com/redis/redis-py)
1. Package manager: [uv](https://github.com/astral-sh/uv) (python versions, python dependencies management) and, of course, brew (for system things)
1. Authentication and authorization: [Keycloak](https://github.com/keycloak/keycloak) for authentication, [Apisix](https://github.com/apache/apisix) + [Keycloak](https://github.com/keycloak/keycloak) for authorization, inter-service authentication should be built on mTLS ([Apisix](https://github.com/apache/apisix) + [Keycloak](https://github.com/keycloak/keycloak) + [Istio](https://github.com/istio/istio))
1. Python performance optimization: [PyPy](https://pypy.org) or [pyston](https://pypi.org/project/pyston-lite-autoload/)
1. DevOps encyclopedia: [CNCF landscape](https://landscape.cncf.io/)
1. Microservices references: [Microservices.io](https://microservices.io/) and [system design primer](https://github.com/donnemartin/system-design-primer)
1. Our logger: [structlog](https://www.structlog.org/en/stable/) with [memory handler](https://docs.python.org/3/library/logging.handlers.html#memoryhandler) (fastest logging)
1. For caching: [rust based cache package](https://github.com/awolverp/cachebox)
1. For validation: [pydantic](https://docs.pydantic.dev/latest/) or [msgspec](https://github.com/jcrist/msgspec)
1. Multiprocessing can be replaced with [mpire](https://github.com/sybrenjansen/mpire)
1. Async boilerplating: [aiorun](https://github.com/cjrh/aiorun)
1. For cli: [typer](https://typer.tiangolo.com/)
1. Check for file type: [python-magic](https://github.com/ahupp/python-magic) & [magika](https://github.com/google/magika) (since latest isn't 100% sure for mimes)
