from __future__ import annotations
import ast
import sys
import typing
from importlib import util as importlib_util
from typing import Final

from community_of_python_flake8_plugin.constants import ALLOWED_STDLIB_FROM_IMPORTS
from community_of_python_flake8_plugin.violation_codes import ViolationCode
from community_of_python_flake8_plugin.violations import Violation


def check_is_stdlib_module(module_name: str) -> bool:
    return module_name in sys.stdlib_module_names


def check_is_stdlib_package(module_name: str) -> bool:
    if not check_is_stdlib_module(module_name):
        return False
    module_spec: Final = importlib_util.find_spec(module_name)
    return module_spec is not None and module_spec.submodule_search_locations is not None


@typing.final
class COP002Check(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def visit_ImportFrom(self, ast_node: ast.ImportFrom) -> None:
        if ast_node.module and ast_node.level == 0 and ast_node.module not in ALLOWED_STDLIB_FROM_IMPORTS:
            self.validate_stdlib_import(ast_node)
        self.generic_visit(ast_node)

    def validate_stdlib_import(self, ast_node: ast.ImportFrom) -> None:
        if ast_node.module == "__future__":
            return
        if (check_is_stdlib_module(ast_node.module) and not check_is_stdlib_package(ast_node.module)) or (
            "." in ast_node.module and check_is_stdlib_package(ast_node.module.split(".")[0])
        ):
            self.violations.append(Violation(ast_node.lineno, ast_node.col_offset, ViolationCode.STDLIB_IMPORT))
