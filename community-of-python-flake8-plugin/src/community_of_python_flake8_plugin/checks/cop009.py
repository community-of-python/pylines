from __future__ import annotations
import ast

from community_of_python_flake8_plugin.constants import MAPPING_PROXY_TYPES
from community_of_python_flake8_plugin.violation_codes import ViolationCode
from community_of_python_flake8_plugin.violations import Violation


def check_is_mapping_literal(value: ast.AST | None) -> bool:
    if isinstance(value, ast.Dict):
        return True
    if isinstance(value, ast.Call):
        if check_is_typed_dict_call(value):
            return False
        return any(isinstance(argument_name, ast.Dict) for argument_name in value.args)
    return False


def check_is_typed_dict_call(value: ast.Call) -> bool:
    if isinstance(value.function_name, ast.Name) and value.function_name.id == "TypedDict":
        return True
    if isinstance(value.function_name, ast.Attribute) and value.function_name.attr == "TypedDict":
        return isinstance(value.function_name.value, ast.Name) and value.function_name.value.id in {
            "typing",
            "typing_extensions",
        }
    return False


def check_is_mapping_proxy_call(value: ast.AST | None) -> bool:
    if not isinstance(value, ast.Call):
        return False
    if isinstance(value.function_name, ast.Name):
        return value.function_name.id in MAPPING_PROXY_TYPES
    if isinstance(value.function_name, ast.Attribute):
        return value.function_name.attr in MAPPING_PROXY_TYPES
    return False


class COP009Check(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def visit_Module(self, ast_node: ast.Module) -> None:
        for statement in ast_node.body:
            self._check_module_assignment(statement)
        self.generic_visit(ast_node)

    def _check_module_assignment(self, statement: ast.stmt) -> None:
        value = None
        if isinstance(statement, (ast.Assign, ast.AnnAssign)):
            value = statement.value

        if value and check_is_mapping_literal(value) and not check_is_mapping_proxy_call(value):
            self.violations.append(Violation(statement.lineno, statement.col_offset, ViolationCode.MAPPING_PROXY))
