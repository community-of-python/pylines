from __future__ import annotations
import ast
import typing

from community_of_python_flake8_plugin.violation_codes import ViolationCode
from community_of_python_flake8_plugin.violations import Violation


def check_is_ignored_name(identifier: str) -> bool:
    if identifier == "_":
        return True
    if identifier.isupper():
        return True
    if identifier in {"value", "values", "pattern"}:
        return True
    if identifier.startswith("__") and identifier.endswith("__"):
        return True
    return bool(identifier.startswith("_"))


def check_is_property(ast_node: ast.AST) -> bool:
    if not isinstance(ast_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    return any(check_is_property_decorator(decorator) for decorator in ast_node.decorator_list)


def check_is_property_decorator(decorator: ast.expr) -> bool:
    if isinstance(decorator, ast.Name):
        return decorator.id == "property"
    if isinstance(decorator, ast.Attribute) and decorator.attr in {"property", "setter", "cached_property"}:
        if isinstance(decorator.value, ast.Name) and decorator.value.id == "functools":
            return decorator.attr == "cached_property"
        return decorator.attr in {"property", "setter"}
    return False


def check_is_pytest_fixture(ast_node: ast.AST) -> bool:
    if not isinstance(ast_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    return any(check_is_fixture_decorator(decorator) for decorator in ast_node.decorator_list)


def check_is_fixture_decorator(decorator: ast.expr) -> bool:
    target: typing.Final = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Name):
        return target.id == "fixture"
    if isinstance(target, ast.Attribute):
        return target.attr == "fixture" and isinstance(target.value, ast.Name) and target.value.id == "pytest"
    return False


class COP006Check(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def visit_AsyncFunctionDef(self, ast_node: ast.AsyncFunctionDef) -> None:
        self._check_get_prefix(ast_node)
        self.generic_visit(ast_node)

    def _check_get_prefix(self, ast_node: ast.AsyncFunctionDef) -> None:
        if check_is_property(ast_node) or check_is_pytest_fixture(ast_node):
            return
        if check_is_ignored_name(ast_node.name):
            return
        if ast_node.name.startswith("get_"):
            self.violations.append(Violation(ast_node.lineno, ast_node.col_offset, ViolationCode.ASYNC_GET_PREFIX))
