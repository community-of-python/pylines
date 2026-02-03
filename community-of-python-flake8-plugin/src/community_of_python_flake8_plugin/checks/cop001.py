from __future__ import annotations
import ast
import typing
from importlib import util as importlib_util
from typing import Final

from community_of_python_flake8_plugin.violation_codes import ViolationCode
from community_of_python_flake8_plugin.violations import Violation


def check_module_path_exists(module_name: str) -> bool:
    try:
        return importlib_util.find_spec(module_name) is not None
    except (ModuleNotFoundError, ValueError):
        return False


MAX_IMPORT_NAMES: Final = 2


@typing.final
class COP001Check(ast.NodeVisitor):
    def __init__(self, contains_all_declaration: bool) -> None:
        self.contains_all_declaration = contains_all_declaration
        self.violations: list[Violation] = []

    def visit_ImportFrom(self, ast_node: ast.ImportFrom) -> None:
        if ast_node.module and ast_node.level == 0:
            self.validate_import_size(ast_node)
        self.generic_visit(ast_node)

    def validate_import_size(self, ast_node: ast.ImportFrom) -> None:
        if len(ast_node.names) <= MAX_IMPORT_NAMES:
            return
        if self.contains_all_declaration:
            return
        if ast_node.module.endswith(".settings"):
            return

        contains_module_import: Final = any(
            isinstance(identifier, ast.alias) and check_module_path_exists(f"{ast_node.module}.{identifier.identifier}")
            for identifier in ast_node.names
        )
        if not contains_module_import:
            self.violations.append(
                Violation(
                    ast_node.lineno,
                    ast_node.col_offset,
                    ViolationCode.MODULE_IMPORT,
                )
            )
