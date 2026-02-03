from __future__ import annotations
import ast
import importlib.util

from community_of_python_flake8_plugin.violation_codes import ViolationCode
from community_of_python_flake8_plugin.violations import Violation


def is_module_path(module_name: str) -> bool:
    try:
        return importlib.util.find_spec(module_name) is not None
    except (ModuleNotFoundError, ValueError):
        return False


class COP001Check(ast.NodeVisitor):
    def __init__(self, module_has_all: bool) -> None:
        self.module_has_all = module_has_all
        self.violations: list[Violation] = []

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module and node.level == 0:
            self._check_import_size(node)
        self.generic_visit(node)

    def _check_import_size(self, node: ast.ImportFrom) -> None:
        if len(node.names) <= 2:
            return
        if self.module_has_all:
            return
        if node.module.endswith(".settings"):
            return

        has_module_import = any(
            isinstance(name, ast.alias) and is_module_path(f"{node.module}.{name.name}") for name in node.names
        )
        if not has_module_import:
            self.violations.append(
                Violation(
                    node.lineno,
                    node.col_offset,
                    ViolationCode.MODULE_IMPORT,
                )
            )
