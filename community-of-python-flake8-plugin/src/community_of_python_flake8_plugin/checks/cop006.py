from __future__ import annotations

import ast

from community_of_python_flake8_plugin.constants import FINAL_CLASS_EXCLUDED_BASES, VERB_PREFIXES
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


def is_verb_name(name: str) -> bool:
    return any(name == verb or name.startswith(f"{verb}_") for verb in VERB_PREFIXES)


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


def inherits_from_whitelisted_class(node: ast.ClassDef) -> bool:
    for base in node.bases:
        if isinstance(base, ast.Name) and base.id in FINAL_CLASS_EXCLUDED_BASES:
            return True
        if isinstance(base, ast.Attribute) and base.attr in FINAL_CLASS_EXCLUDED_BASES:
            return True
    return False


def get_parent_class(tree: ast.AST, node: ast.AST) -> ast.ClassDef | None:
    for potential_parent in ast.walk(tree):
        if isinstance(potential_parent, ast.ClassDef):
            for child in ast.walk(potential_parent):
                if child is node:
                    return potential_parent
    return None


class COP006Check(ast.NodeVisitor):
    def __init__(self, tree: ast.AST) -> None:
        self.tree = tree
        self.violations: list[Violation] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._check_function(node)
        self.generic_visit(node)

    def _check_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        if is_pytest_fixture(node):
            return
        if node.name == "main":
            return
        if is_property(node):
            return
        if is_ignored_name(node.name):
            return
        if node.name.startswith("test_"):
            return
        
        # Check if function is inside a class that inherits from whitelisted class
        parent_class = get_parent_class(self.tree, node)
        if parent_class and inherits_from_whitelisted_class(parent_class):
            return
            
        if not is_verb_name(node.name):
            self.violations.append(Violation(node.lineno, node.col_offset, "COP006 Function name must be a verb"))