Code style
---

Setup
-----
1. `pip install ruff`
1. Add following config in the `pyproject.toml`:
    ```toml
    [tool.ruff]
    fix = true
    unsafe-fixes = true
    line-length = 120

    [tool.ruff.format]
    docstring-code-format = true

    [tool.ruff.lint]
    select = ["ALL"]
    ignore = ["EM", "FBT", "TRY003", "D1", "D203", "D213", "G004", "FA", "COM812", "ISC001"]

    [tool.ruff.lint.isort]
    no-lines-before = ["standard-library", "local-folder"]
    known-third-party = []
    known-local-folder = []
    lines-after-imports = 2

    [tool.ruff.lint.extend-per-file-ignores]
    "tests/*.py" = ["S101", "S311"]

    [tool.coverage.report]
    exclude_also = ["if typing.TYPE_CHECKING:"]
    ```


Rules
-----
1. Code length is 120 symbols
1. 
