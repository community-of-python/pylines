# Recommended solutions

This is a list of libraries, frameworks, infrastructure solutions, and references we choose:

1. Our frameworks: [FastAPI](https://github.com/tiangolo/fastapi) and [Litestar](https://github.com/litestar-org/litestar)  
2. For basic service boilerplating: [microbootstrap](https://github.com/community-of-python/microbootstrap)  
3. Our logger: [structlog](https://www.structlog.org/en/stable/)  
4. Python application server: [granian](https://github.com/emmett-framework/granian) (instead of Uvicorn)  
5. DI frameworks: [that depends](https://github.com/modern-python/that-depends), [modern di](https://github.com/modern-python/modern-di/), or [dishka](https://github.com/reagento/dishka)  
6. ORM: SQLAlchemy  
7. Our testing suite: pytest, [pytest-xdist](https://github.com/pytest-dev/pytest-xdist), [hypothesis](https://github.com/HypothesisWorks/hypothesis), [schemathesis](https://github.com/schemathesis/schemathesis), [polyfactory](https://polyfactory.litestar.dev/latest/), faker  
8. Event-driven architecture: [faststream](https://github.com/airtai/faststream) (combine with transactional outbox/inbox for greater reliability)  
9. Configuration management: [pydantic settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)  
10. HTTP clients: [httpx](https://www.python-httpx.org/) or [niquests](https://niquests.readthedocs.io/en/latest/)  
11. File operations: [aiofile](https://github.com/mosquito/aiofile)  
12. Metrics and observability: [open telemetry](https://opentelemetry.io/docs/languages/python/), for some services you can [use automatic/zero-code instrumentation](https://opentelemetry.io/docs/zero-code/python/)  
13. For background tasks: [taskiq](https://github.com/taskiq-python/taskiq)  
14. Linters and formatters: ruff (check, format, fix modes are all useful) and mypy (we heavily use the [typing](https://docs.python.org/3/library/typing.html) library)  
15. Our NoSQL databases: [valkey](https://valkey.io/) or [dragonfly](https://www.dragonflydb.io/); for accessing them, we use asynchronous [Redis py](https://github.com/redis/redis-py)  
16. Package manager: uv (+ Python version management)  
17. Authentication and authorization: Keycloak for authentication, Apisix + Keycloak for authorization, inter-service authentication should be built on mTLS (Apisix + Istio)  
18. Python performance optimization: PyPy  
19. DevOps encyclopedia: [CNCF landscape](https://landscape.cncf.io/)  
20. Microservices references: [Microservices.io](https://microservices.io/) and [system design primer](https://github.com/donnemartin/system-design-primer)  
