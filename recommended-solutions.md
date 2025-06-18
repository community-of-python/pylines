# Recommended solutions

This is a list of libraries, frameworks, infrastructure solutions, and references we choose:

1. Our frameworks: [Litestar](https://github.com/litestar-org/litestar) (main, prefferred) and [FastAPI](https://github.com/tiangolo/fastapi) (secondary)
1. For basic service boilerplating is a must: [microbootstrap](https://github.com/community-of-python/microbootstrap)  
1. Python application server: [granian](https://github.com/emmett-framework/granian) (instead of Uvicorn)  
1. DI frameworks: [that depends](https://github.com/modern-python/that-depends), [modern di](https://github.com/modern-python/modern-di/), or [dishka](https://github.com/reagento/dishka)  
1. ORM: SQLAlchemy  
1. Our testing suite: pytest, [pytest-xdist](https://github.com/pytest-dev/pytest-xdist), [hypothesis](https://github.com/HypothesisWorks/hypothesis), [schemathesis](https://github.com/schemathesis/schemathesis), [polyfactory](https://polyfactory.litestar.dev/latest/), faker  
1. Event-driven architecture: [faststream](https://github.com/airtai/faststream) (combine with transactional outbox/inbox for greater reliability)  
1. Configuration management: [pydantic settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)  
1. HTTP clients: [httpx](https://www.python-httpx.org/) or [niquests](https://niquests.readthedocs.io/en/latest/) (in wich streaming is broken, be careful)  
1. File operations: [aiofile](https://github.com/mosquito/aiofile) (differs from aiofile**s**)  
1. Metrics and observability: [open telemetry](https://opentelemetry.io/docs/languages/python/), for some services you can [use automatic/zero-code instrumentation](https://opentelemetry.io/docs/zero-code/python/)  
1. For background tasks: [taskiq](https://github.com/taskiq-python/taskiq)  
1. Linters and formatters: ruff (check, format, fix modes are all useful) and mypy (we heavily use the [typing](https://docs.python.org/3/library/typing.html) library)  
2. Our NoSQL databases: redis, or [valkey](https://valkey.io/)/[dragonfly](https://www.dragonflydb.io/); for accessing them, we use asynchronous [Redis py](https://github.com/redis/redis-py)  
3. Package manager: uv (+ Python version management)  
4. Authentication and authorization: Keycloak for authentication, Apisix + Keycloak for authorization, inter-service authentication should be built on mTLS (Apisix + Istio)  
5. Python performance optimization: PyPy  
6. DevOps encyclopedia: [CNCF landscape](https://landscape.cncf.io/)  
7. Microservices references: [Microservices.io](https://microservices.io/) and [system design primer](https://github.com/donnemartin/system-design-primer)  
8. Our logger: [structlog](https://www.structlog.org/en/stable/)  
9. For caching [rust based cache package](https://github.com/awolverp/cachebox)
