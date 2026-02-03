from __future__ import annotations

import ast

from community_of_python_flake8_plugin.constants import FINAL_CLASS_EXCLUDED_BASES, MIN_NAME_LENGTH
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


def inherits_from_whitelisted_class(node: ast.ClassDef) -> bool:
    for base in node.bases:
        if isinstance(base, ast.Name) and base.id in FINAL_CLASS_EXCLUDED_BASES:
            return True
        if isinstance(base, ast.Attribute) and base.attr in FINAL_CLASS_EXCLUDED_BASES:
            return True
    return False


def is_whitelisted_annotation(annotation: ast.expr | None) -> bool:
    if annotation is None:
        return False
    if isinstance(annotation, ast.Name):
        return annotation.id in {"fixture", "Faker"}
    if isinstance(annotation, ast.Attribute):
        if isinstance(annotation.value, ast.Name):
            return annotation.value.id in {"pytest", "faker"}
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


def get_parent_class(tree: ast.AST, node: ast.AST) -> ast.ClassDef | None:
    for potential_parent in ast.walk(tree):
        if isinstance(potential_parent, ast.ClassDef):
            for child in ast.walk(potential_parent):
                if child is node:
                    return potential_parent
    return None


class COP005Check(ast.NodeVisitor):
    def __init__(self, tree: ast.AST) -> None:
        self.tree = tree
        self.violations: list[Violation] = []

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if isinstance(node.target, ast.Name):
            parent_class = get_parent_class(self.tree, node)
            self._check_name_length(node.target.id, node, parent_class)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            if isinstance(target, ast.Name):
                parent_class = get_parent_class(self.tree, node)
                self._check_name_length(target.id, node, parent_class)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        parent_class = get_parent_class(self.tree, node)
        self._check_function_name(node, parent_class)
        self._check_function_args(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        parent_class = get_parent_class(self.tree, node)
        self._check_function_name(node, parent_class)
        self._check_function_args(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        if not node.name.startswith("Test"):
            self._check_class_name_length(node)
        self.generic_visit(node)

    def _check_name_length(self, name: str, node: ast.AST, parent_class: ast.ClassDef | None) -> None:
        if is_ignored_name(name):
            return
        # Only apply parent class exemption for assignments within classes
        if parent_class and isinstance(node, (ast.AnnAssign, ast.Assign)):
            if inherits_from_whitelisted_class(parent_class):
                return
        if len(name) < MIN_NAME_LENGTH:
            self.violations.append(Violation(node.lineno, node.col_offset, "COP005 Name must be at least 8 characters"))

    def _check_function_name(self, node: ast.FunctionDef | ast.AsyncFunctionDef, parent_class: ast.ClassDef | None) -> None:
        if is_pytest_fixture(node):
            return
        if node.name == "main":
            return
        if is_ignored_name(node.name):
            return
        if parent_class and inherits_from_whitelisted_class(parent_class):
            return
        if len(node.name) < MIN_NAME_LENGTH:
            self.violations.append(Violation(node.lineno, node.col_offset, "COP005 Name must be at least 8 characters"))

    def _check_function_args(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        arguments = node.args
        for argument in arguments.posonlyargs + arguments.args + arguments.kwonlyargs:
            self._check_argument_name_length(argument)
        if arguments.vararg is not None:
            self._check_argument_name_length(arguments.vararg)
        if arguments.kwarg is not None:
            self._check_argument_name_length(arguments.kwarg)

    def _check_argument_name_length(self, argument: ast.arg) -> None:
        if argument.arg in {"self", "cls"}:
            return
        if is_ignored_name(argument.arg):
            return
        if is_whitelisted_annotation(argument.annotation):
            return
        if len(argument.arg) < MIN_NAME_LENGTH:
            self.violations.append(Violation(argument.lineno, argument.col_offset, "COP005 Name must be at least 8 characters"))

    def _check_class_name_length(self, node: ast.ClassDef) -> None:
        if is_ignored_name(node.name):
            return
        if len(node.name) < MIN_NAME_LENGTH:
            self.violations.append(Violation(node.lineno, node.col_offset, "COP005 Name must be at least 8 characters"))