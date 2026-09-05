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

# Python Guidelines (pylines) — live from GitHub

Source of truth: [community-of-python/pylines](https://github.com/community-of-python/pylines).
Guides are NOT bundled in this skill — they are pulled from GitHub and cached locally.

## Step 0 — always run first

```bash
bash "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/python-guidelines}/sync.sh"
```

Shallow `fetch` + `reset --hard` into `cache/pylines/`, at most once per hour
(`PYLINES_TTL_MIN` overrides; within the TTL it exits without touching the network).
Prints the cache path and short commit. Offline-safe: on network failure it keeps the
last cached copy and says so. Use the printed path — do not hardcode it.

## Step 1 — read the relevant guide from cache

Read only what the task needs. `solid.md` is ~62 KB and `code-style.md` ~21 KB — never read
either whole. Locate first, then read a range:

```bash
rg -n --heading "<term>" <cache>/*.md   # then Read the file with offset/limit, ±30 lines
```

| Тема | Файл |
|------|------|
| Стиль кода, типизация, именование, иммутабельность, исключения, импорты | `code-style.md` |
| REST API, URL conventions, версионирование | `rest.md` |
| Тесты: AAA, parametrize, faker/hypothesis, pytest-xdist | `tests.md` |
| SOLID с примерами на Python | `solid.md` |
| Рекомендуемые библиотеки и инструменты | `our-stack.md` |
| Архитектура | `architecture-guide.md` |
| Эталонный ruff/mypy/flake8 конфиг | `pyproject.toml` |

## Minimal always-on rules (details in the cached guides)

- Tooling: **ruff** (`select = ALL`), **mypy --strict**, **uv**, line length **120**, server **granian**.
- Typing: 100% annotations, `typing.Final` on vars, `@typing.final` on classes, narrow types (Literal/TypedDict).
- Naming: verbs for functions, no `get` prefix (use fetch/build/parse…), names ≥ 8 chars, semantic.
- Classes: composition over inheritance; `@dataclass(kw_only=True, slots=True, frozen=True)`; `typing.Protocol` for interfaces.
- Exceptions: catch concrete types, LBYL over EAFP, narrow try-blocks.
- Resilience: retry anything leaving RAM (SQL/HTTP/files) via **stamina**.
- Read the matching cached guide before quoting specifics — this list is a pointer, not the standard.
