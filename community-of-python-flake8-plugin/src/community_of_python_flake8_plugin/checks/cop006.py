from __future__ import annotations

import ast

from community_of_python_flake8_plugin.violations import Violation


def is_ignored_name(name: str) -> bool:
    if name == "_":
        return True
    if name.isupper():
        return True
    if name in {"value", "values", "pattern"}:
        return True
    if name.startswith("__") and name.endswith("__"):
        return True
    if name.startswith("_"):
        return True
    return False


def is_property(node: ast.AST) -> bool:
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    return any(is_property_decorator(decorator) for decorator in node.decorator_list)


def is_property_decorator(decorator: ast.expr) -> bool:
    if isinstance(decorator, ast.Name):
        return decorator.id == "property"
    if isinstance(decorator, ast.Attribute):
        if decorator.attr in {"property", "setter", "cached_property"}:
            if isinstance(decorator.value, ast.Name) and decorator.value.id == "functools":
                return decorator.attr == "cached_property"
            return decorator.attr == "property" or decorator.attr == "setter"
    return False


def is_pytest_fixture(node: ast.AST) -> bool:
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    return any(is_fixture_decorator(decorator) for decorator in node.decorator_list)


def is_fixture_decorator(decorator: ast.expr) -> bool:
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Name):
        return target.id == "fixture"
    if isinstance(target, ast.Attribute):
        return target.attr == "fixture" and isinstance(target.value, ast.Name) and target.value.id == "pytest"
    return False


class COP006Check(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._check_get_prefix(node)
        self.generic_visit(node)

    def _check_get_prefix(self, node: ast.AsyncFunctionDef) -> None:
        if is_property(node) or is_pytest_fixture(node):
            return
        if is_ignored_name(node.name):
            return
        if node.name.startswith("get_"):
            self.violations.append(Violation(node.lineno, node.col_offset, "COP006 Avoid get_ prefix in async function names"))