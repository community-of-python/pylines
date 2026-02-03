from __future__ import annotations
import ast
import importlib.util
import sys

from community_of_python_flake8_plugin.constants import ALLOWED_STDLIB_FROM_IMPORTS
from community_of_python_flake8_plugin.violation_codes import ViolationCode
from community_of_python_flake8_plugin.violations import Violation


def is_stdlib_module(module_name: str) -> bool:
    return module_name in sys.stdlib_module_names


def is_stdlib_package(module_name: str) -> bool:
    if not is_stdlib_module(module_name):
        return False
    spec = importlib.util.find_spec(module_name)
    return spec is not None and spec.submodule_search_locations is not None


class COP002Check(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module and node.level == 0 and node.module not in ALLOWED_STDLIB_FROM_IMPORTS:
            self._check_stdlib_import(node)
        self.generic_visit(node)

    def _check_stdlib_import(self, node: ast.ImportFrom) -> None:
        if node.module == "__future__":
            return
        (
            is_stdlib_module(node.module) and not is_stdlib_package(node.module)
        ) or (
            "." in node.module and is_stdlib_package(node.module.split(".")[0])
        ):
            self.violations.append(
                Violation(node.lineno, node.col_offset, ViolationCode.STDLIB_IMPORT)
            )
