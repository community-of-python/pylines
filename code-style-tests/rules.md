# Code Style Rules Checklist (automatable targets)

- [x] **PEP Compliance**
    - [x] PEP 8 (covered by ruff)
    - [x] PEP 257 (for docstrings)
    - [x] PEP 526 (Syntax for Variable Annotations)
    - [x] PEP 484 (Type Hints) (mypy)
- [x] **Line Length**: 120 characters
- [x] **Import Rules**
    - [x] Import built-in libraries as a whole (e.g., `import os`)
    - [x] Import modules with more than 2 imports as a whole (e.g., `import my_module`)
- [x] **Exception Handling**
    - [x] Avoid `except Exception`; use specific exception classes.
- [x] **Variable Usage**: Avoid creating temporary variables without a good reason (improving readability or reuse).
