from __future__ import annotations

import ast
import importlib.util
import sys

from community_of_python_flake8_plugin.constants import ALLOWED_STDLIB_FROM_IMPORTS
from community_of_python_flake8_plugin.violations import Violation


def is_stdlib_module(module_name: str) -> bool:
    return module_name in sys.stdlib_module_names


def is_stdlib_package(module_name: str) -> bool:
    if not is_stdlib_module(module_name):
        return False
    spec = importlib.util.find_spec(module_name)
    return spec is not None and spec.submodule_search_locations is not None


def is_module_path(module_name: str) -> bool:
    try:
        return importlib.util.find_spec(module_name) is not None
    except (ModuleNotFoundError, ValueError):
        return False


class ImportCheck(ast.NodeVisitor):
    def __init__(self, module_has_all: bool) -> None:
        self.module_has_all = module_has_all
        self.violations: list[Violation] = []

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module and node.level == 0:
            if node.module not in ALLOWED_STDLIB_FROM_IMPORTS:
                self._check_import_size(node)
                self._check_stdlib_import(node)
        self.generic_visit(node)

    def _check_import_size(self, node: ast.ImportFrom) -> None:
        if len(node.names) <= 2:
            return
        if self.module_has_all:
            return
        if node.module.endswith(".settings"):
            return

        has_module_import = any(
            isinstance(name, ast.alias) and is_module_path(f"{node.module}.{name.name}")
            for name in node.names
        )
        if not has_module_import:
            self.violations.append(
                Violation(
                    node.lineno,
                    node.col_offset,
                    "COP001 Use module import when importing more than two names",
                )
            )

    def _check_stdlib_import(self, node: ast.ImportFrom) -> None:
        if node.module == "__future__":
            return
        if is_stdlib_module(node.module) and not is_stdlib_package(node.module):
            self.violations.append(
                Violation(node.lineno, node.col_offset, "COP002 Import standard library modules as whole modules")
            )
        elif "." in node.module and is_stdlib_package(node.module.split(".")[0]):
            self.violations.append(
                Violation(node.lineno, node.col_offset, "COP002 Import standard library modules as whole modules")
            )
