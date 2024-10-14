Code style
---
This code style aims to do the following: make your life easier through auto-formatting, be as simple as possible without any hidden paths or tools. This is a straightforward guide for achieving good code quality, tailored for any "lazy" (in a good way) developers who don't want to bother

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
1. All built-in libraries should be imported in full (`import os`, `import typing`), as well as modules from which more than 2 any objects are imported (`from my_module import SomeModule, AnotherModule, HelloOne` ==> `import my_module`)
1. ...
