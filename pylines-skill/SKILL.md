---
name: pylines
description: >
  Development guidelines from the pylines project (community-of-python/pylines) — Python backend
  and TypeScript/React frontend. Use whenever writing, reviewing, or refactoring code in either:
  backend work with FastAPI, Litestar, SQLAlchemy, or frontend work with React, TypeScript, styles.
  Trigger on any code generation, code review, architecture discussion, REST API design, test
  writing, or when the user mentions "pylines", "code style", "наши гайдлайны", "guidelines", or
  asks to follow team conventions. Also trigger when writing pyproject.toml configs for ruff/mypy,
  designing class hierarchies, discussing SOLID, or structuring a project.
---

# Guidelines (pylines) — live from GitHub

Source of truth: [community-of-python/pylines](https://github.com/community-of-python/pylines).
The guides are NOT bundled here — they are pulled from GitHub and cached locally, so this file
never goes stale against them.

## Step 0 — always run first

Run `sync.sh`, which sits in the same directory as this file:

```bash
bash <this-directory>/sync.sh
```

It shallow-fetches the repo into `cache/pylines/` next to the script, at most once an hour
(`PYLINES_TTL_MIN` overrides the interval; `0` forces a fetch). On network failure it keeps the
last cached copy and says so, so this works offline.

It prints two paths — the guides directory and `index.md`. Use the printed paths, do not hardcode
them.

## Step 1 — read the relevant guide

Pick the file from the table below, then:

- **Every guide except `solid.md`: read it whole.** They run 3–245 lines; a partial read cuts a
  rule away from the ❌/✅ example that defines it, which is worse than reading the extra lines.
- **`solid.md` (703 lines): read `index.md` first.** `sync.sh` regenerates it on every run — it
  lists each guide's headings with line numbers, so you can read just the principle you need
  (SRP, OCP, LSP, ISP, DIP are ~100 lines each) instead of the whole file.

If you cannot find a rule, say so and read the guide whole. Never answer from memory about what
these guides say — that is exactly what the cache exists to prevent.

| Тема | Файл |
|------|------|
| Python: стиль, типизация, именование, иммутабельность, исключения, импорты | `code-style.md` |
| Python: REST API, URL conventions, версионирование | `rest.md` |
| Python: тесты — AAA, parametrize, faker/hypothesis, pytest-xdist | `tests.md` |
| Python: SOLID с примерами | `solid.md` |
| Python: рекомендуемые библиотеки и инструменты | `our-stack.md` |
| Python: архитектура | `architecture-guide.md` |
| Python: эталонный ruff/mypy/flake8 конфиг | `pyproject.toml` |
| Frontend: TypeScript, React, стили, именование, комментарии | `frontend.md` |
| Frontend: визуальные правила генерации UI — шрифты, отступы, акценты, выравнивание | `frontend-generation.md` |

## Minimal always-on rules (details in the cached guides)

Python:

- Tooling: **ruff** (`select = ALL`), **mypy --strict**, **uv**, line length **120**, server **granian**.
- Typing: 100% annotations, `typing.Final` on vars, `@typing.final` on classes, narrow types (Literal/TypedDict).
- Naming: verbs for functions, no `get` prefix (use fetch/build/parse…), names ≥ 8 chars, semantic.
- Classes: composition over inheritance; `@dataclass(kw_only=True, slots=True, frozen=True)`; `typing.Protocol` for interfaces.
- Exceptions: catch concrete types, LBYL over EAFP, narrow try-blocks.
- Resilience: retry anything leaving RAM (SQL/HTTP/files) via **stamina**.

Frontend:

- Styles: **styled-components**; classes follow BEM; no `font-face` — wrap the layout in `Body` from the Design System, one font-face per project. Take values from DS tokens.
- React: hooks everywhere, `useEffect` with explicit deps, wrap in-component functions in `useCallback`.
- Component body order: `const` block → blank line → `useEffect` block → blank line → JSX.
- No shorthand casts (`!!x`, `~x`, `+x`) — cast explicitly. No prop drilling. Magic numbers → constants.
- Naming: identifiers ≥ 8 chars, verbs for functions, arrow functions only; `lowerCamelCase` vars/functions, `UpperCamelCase` types, `UPPER_CASE` constants. `data`, `user`, `variable` are banned.

Applies to both: read the matching cached guide before quoting specifics — these lists are pointers, not the standard.
