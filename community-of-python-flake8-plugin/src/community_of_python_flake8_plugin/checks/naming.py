from __future__ import annotations

import ast

from community_of_python_flake8_plugin.constants import MIN_NAME_LENGTH
from community_of_python_flake8_plugin.helpers import is_ignored_name, is_property, is_pytest_fixture, is_verb_name
from community_of_python_flake8_plugin.violations import Violation


def check_name_length(name: str, node: ast.AST) -> list[Violation]:
    if is_ignored_name(name):
        return []
    if is_pytest_fixture(node):
        return []
    if len(name) < MIN_NAME_LENGTH:
        return [Violation(node.lineno, node.col_offset, "COP005 Name must be at least 8 characters")]
    return []


def check_attribute_name_length(node: ast.AST) -> list[Violation]:
    if not isinstance(node, ast.AnnAssign):
        return []
    if node.value is None:
        return []
    if not isinstance(node.target, ast.Attribute):
        return []
    name = node.target.attr
    if is_ignored_name(name):
        return []
    if len(name) < MIN_NAME_LENGTH:
        return [Violation(node.lineno, node.col_offset, "COP005 Name must be at least 8 characters")]
    return []


def check_function_verb(node: ast.AST) -> list[Violation]:
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return []
    if is_property(node) or is_pytest_fixture(node):
        return []
    if is_ignored_name(node.name) or node.name.startswith("test_"):
        return []
    if not is_verb_name(node.name):
        return [Violation(node.lineno, node.col_offset, "COP006 Function name must be a verb")]
    return []


def check_get_prefix(node: ast.AST) -> list[Violation]:
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return []
    if is_property(node) or is_pytest_fixture(node):
        return []
    if is_ignored_name(node.name):
        return []
    if node.name.startswith("get_"):
        return [Violation(node.lineno, node.col_offset, "COP007 Avoid get_ prefix in function names")]
    return []
