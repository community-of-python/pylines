from __future__ import annotations

import ast

from community_of_python_flake8_plugin.checks.annotation_check import AnnotationCheck
from community_of_python_flake8_plugin.checks.class_check import ClassCheck
from community_of_python_flake8_plugin.checks.import_check import ImportCheck
from community_of_python_flake8_plugin.checks.module_check import ModuleCheck
from community_of_python_flake8_plugin.checks.naming_check import NamingCheck
from community_of_python_flake8_plugin.checks.temporary_var_check import TemporaryVarCheck
from community_of_python_flake8_plugin.constants import MIN_NAME_LENGTH
from community_of_python_flake8_plugin.violations import Violation


def module_has_all(node: ast.Module) -> bool:
    for statement in node.body:
        if isinstance(statement, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "__all__" for target in statement.targets):
                return True
        if isinstance(statement, ast.AnnAssign):
            if isinstance(statement.target, ast.Name) and statement.target.id == "__all__":
                return True
    return False


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


def check_name_length(name: str, node: ast.AST) -> list[Violation]:
    if is_ignored_name(name):
        return []
    if len(name) < MIN_NAME_LENGTH:
        return [Violation(node.lineno, node.col_offset, "COP005 Name must be at least 8 characters")]
    return []


def get_parent_class(tree: ast.AST, node: ast.AST) -> ast.ClassDef | None:
    for potential_parent in ast.walk(tree):
        if isinstance(potential_parent, ast.ClassDef):
            for child in ast.walk(potential_parent):
                if child is node:
                    return potential_parent
    return None


def get_parent_function(tree: ast.AST, node: ast.AST) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    for potential_parent in ast.walk(tree):
        if isinstance(potential_parent, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for child in ast.walk(potential_parent):
                if child is node:
                    return potential_parent
    return None


def run_all_checks(tree: ast.AST) -> list[Violation]:
    has_all = module_has_all(tree)
    all_violations: list[Violation] = []

    import_check = ImportCheck(has_all)
    import_check.visit(tree)
    all_violations.extend(import_check.violations)

    temporary_var_check = TemporaryVarCheck()
    temporary_var_check.visit(tree)
    all_violations.extend(temporary_var_check.violations)

    class_check = ClassCheck()
    class_check.visit(tree)
    all_violations.extend(class_check.violations)

    module_check = ModuleCheck()
    module_check.visit(tree)
    all_violations.extend(module_check.violations)

    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign):
            parent_class = get_parent_class(tree, node)
            parent_function = get_parent_function(tree, node)
            in_class_body = parent_class is not None and parent_function is None

            annotation_check = AnnotationCheck(in_class_body=in_class_body)
            annotation_check.visit(node)
            all_violations.extend(annotation_check.violations)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            parent_class = get_parent_class(tree, node)
            naming_check = NamingCheck(parent_class)
            naming_check.visit(node)
            all_violations.extend(naming_check.violations)

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            parent_class = get_parent_class(tree, node)
            parent_function = get_parent_function(tree, node)
            if parent_function is not None or (parent_class is None):
                naming_check = NamingCheck(None)
                naming_check.visit(node)
                all_violations.extend(naming_check.violations)

    return all_violations
