from __future__ import annotations

import ast

from community_of_python_flake8_plugin.constants import MAPPING_PROXY_TYPES
from community_of_python_flake8_plugin.violations import Violation


def is_mapping_literal(value: ast.AST | None) -> bool:
    if isinstance(value, ast.Dict):
        return True
    if isinstance(value, ast.Call):
        if is_typed_dict_call(value):
            return False
        return any(isinstance(arg, ast.Dict) for arg in value.args)
    return False


def is_typed_dict_call(value: ast.Call) -> bool:
    if isinstance(value.func, ast.Name) and value.func.id == "TypedDict":
        return True
    if isinstance(value.func, ast.Attribute) and value.func.attr == "TypedDict":
        return isinstance(value.func.value, ast.Name) and value.func.value.id in {"typing", "typing_extensions"}
    return False


def is_mapping_proxy_call(value: ast.AST | None) -> bool:
    if not isinstance(value, ast.Call):
        return False
    if isinstance(value.func, ast.Name):
        return value.func.id in MAPPING_PROXY_TYPES
    if isinstance(value.func, ast.Attribute):
        return value.func.attr in MAPPING_PROXY_TYPES
    return False


class COP009Check(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def visit_Module(self, node: ast.Module) -> None:
        for statement in node.body:
            self._check_module_assignment(statement)
        self.generic_visit(node)

    def _check_module_assignment(self, statement: ast.stmt) -> None:
        value = None
        if isinstance(statement, ast.Assign):
            value = statement.value
        elif isinstance(statement, ast.AnnAssign):
            value = statement.value

        if value and is_mapping_literal(value) and not is_mapping_proxy_call(value):
            self.violations.append(
                Violation(statement.lineno, statement.col_offset, "COP009 Wrap module dictionaries with types.MappingProxyType")
            )