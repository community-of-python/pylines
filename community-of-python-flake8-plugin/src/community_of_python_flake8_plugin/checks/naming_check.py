from __future__ import annotations

import ast

from community_of_python_flake8_plugin.constants import FINAL_CLASS_EXCLUDED_BASES, MIN_NAME_LENGTH, VERB_PREFIXES
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


def inherits_from_whitelisted_class(node: ast.ClassDef) -> bool:
    for base in node.bases:
        if isinstance(base, ast.Name) and base.id in FINAL_CLASS_EXCLUDED_BASES:
            return True
        if isinstance(base, ast.Attribute) and base.attr in FINAL_CLASS_EXCLUDED_BASES:
            return True
    return False


class NamingCheck(ast.NodeVisitor):
    def __init__(self, parent_class: ast.ClassDef | None = None) -> None:
        self.parent_class = parent_class
        self.violations: list[Violation] = []

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.violations.extend(check_name_length(target.id, node, self.parent_class))
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._check_function(node)
        self.generic_visit(node)

    def _check_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        if is_pytest_fixture(node):
            self.violations.extend(check_function_argument_names(node))
            return
        if node.name == "main":
            return
        self.violations.extend(check_name_length(node.name, node, self.parent_class))
        self.violations.extend(check_function_argument_names(node))
        if isinstance(node, ast.AsyncFunctionDef):
            self.violations.extend(check_get_prefix(node))
        if not is_property(node):
            if not is_ignored_name(node.name) and not node.name.startswith("test_"):
                if not (self.parent_class and inherits_from_whitelisted_class(self.parent_class)):
                    if not is_verb_name(node.name):
                        self.violations.append(Violation(node.lineno, node.col_offset, "COP006 Function name must be a verb"))


def check_name_length(name: str, node: ast.AST, parent_class: ast.ClassDef | None = None) -> list[Violation]:
    if is_ignored_name(name):
        return []
    if isinstance(node, ast.FunctionDef) and node.name == "main":
        return []
    if parent_class and inherits_from_whitelisted_class(parent_class):
        return []
    if len(name) < MIN_NAME_LENGTH:
        return [Violation(node.lineno, node.col_offset, "COP005 Name must be at least 8 characters")]
    return []


def check_argument_name_length(argument: ast.arg) -> list[Violation]:
    if argument.arg in {"self", "cls"}:
        return []
    if is_ignored_name(argument.arg):
        return []
    if is_whitelisted_annotation(argument.annotation):
        return []
    if len(argument.arg) < MIN_NAME_LENGTH:
        return [Violation(argument.lineno, argument.col_offset, "COP005 Name must be at least 8 characters")]
    return []


def check_function_argument_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[Violation]:
    violations: list[Violation] = []
    arguments = node.args
    for argument in arguments.posonlyargs + arguments.args + arguments.kwonlyargs:
        violations.extend(check_argument_name_length(argument))
    if arguments.vararg is not None:
        violations.extend(check_argument_name_length(arguments.vararg))
    if arguments.kwarg is not None:
        violations.extend(check_argument_name_length(arguments.kwarg))
    return violations


def check_get_prefix(node: ast.AsyncFunctionDef) -> list[Violation]:
    if is_property(node) or is_pytest_fixture(node):
        return []
    if is_ignored_name(node.name):
        return []
    if node.name.startswith("get_"):
        return [Violation(node.lineno, node.col_offset, "COP007 Avoid get_ prefix in async function names")]
    return []
