from __future__ import annotations

import ast

from community_of_python_flake8_plugin.helpers import (
    is_module_path,
    is_stdlib_module,
    is_stdlib_package,
    module_has_all,
)
from community_of_python_flake8_plugin.violations import Violation


def check_import_from(node: ast.ImportFrom, has_all: bool) -> list[Violation]:
    violations: list[Violation] = []
    if node.module and node.level == 0:
        if len(node.names) > 2 and not has_all and not node.module.endswith(".settings"):
            has_module_import = any(
                isinstance(name, ast.alias) and is_module_path(f"{node.module}.{name.name}")
                for name in node.names
            )
            if not has_module_import:
                violations.append(
                    Violation(
                        node.lineno,
                        node.col_offset,
                        "COP001 Use module import when importing more than two names",
                    )
                )
        if node.module != "__future__" and is_stdlib_module(node.module) and not is_stdlib_package(node.module):
            violations.append(
                Violation(node.lineno, node.col_offset, "COP002 Import standard library modules as whole modules")
            )
        elif "." in node.module and is_stdlib_package(node.module.split(".")[0]):
            violations.append(
                Violation(node.lineno, node.col_offset, "COP002 Import standard library modules as whole modules")
            )
    return violations
