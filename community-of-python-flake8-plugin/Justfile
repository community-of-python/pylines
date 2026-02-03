install:
    uv sync

test *args:
    uv run --group test pytest {{args}}

lint:
    .venv/bin/ruff format
    .venv/bin/ruff check
    .venv/bin/auto-typing-final .
    .venv/bin/flake8 --select COP --exclude .venv .
    cd .. && community-of-python-flake8-plugin/.venv/bin/mypy community-of-python-flake8-plugin
