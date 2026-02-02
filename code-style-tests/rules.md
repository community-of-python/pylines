# Code Style Rules Checklist (automatable)

- [x] **PEP Compliance**
    - [x] PEP 8 (covered by ruff)
    - [x] PEP 484 (Type Hints) (mypy)
- [x] **Line Length**: 120 characters
- [x] **Exception Handling**
    - [x] Avoid `except Exception`; use specific exception classes.
- [x] **Variable Usage**: Avoid creating temporary variables without a good reason (improving readability or reuse).

See `rules-non-automatable.md` for subjective or currently non-automatable rules.
