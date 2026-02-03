# community-of-python-flake8-plugin

Community of Python flake8 plugin with custom code style checks.

## Run with uv

```bash
uv run --with flake8 --with "community-of-python-flake8-plugin @ git+https://github.com/community-of-python/pylines.git@code-style-tests#subdirectory=community-of-python-flake8-plugin" -- flake8 --select COP --exclude .venv .
```

## flake8 config (pyproject.toml)

```toml
[tool.flake8]
select = ["COP"]
exclude = [".venv"]
```
