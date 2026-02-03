from __future__ import annotations
import ast

from community_of_python_flake8_plugin.constants import FINAL_CLASS_EXCLUDED_BASES
from community_of_python_flake8_plugin.violation_codes import ViolationCode
from community_of_python_flake8_plugin.violations import Violation


def check_is_true_literal(ast_node: ast.AST | None) -> bool:
    return isinstance(ast_node, ast.Constant) and ast_node.value is True


def contains_final_decorator(ast_node: ast.ClassDef) -> bool:
    for decorator in ast_node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if isinstance(target, ast.Name) and target.id == "final":
            return True
        if isinstance(target, ast.Attribute) and target.attr == "final":
            return True
    return False


def inherits_from_whitelisted_class(ast_node: ast.ClassDef) -> bool:
    for base_class in ast_node.bases:
        if isinstance(base_class, ast.Name) and base_class.id in FINAL_CLASS_EXCLUDED_BASES:
            return True
        if isinstance(base_class, ast.Attribute) and base_class.attr in FINAL_CLASS_EXCLUDED_BASES:
            return True
    return False


def retrieve_dataclass_decorator(ast_node: ast.ClassDef) -> ast.expr | None:
    for decorator in ast_node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if isinstance(target, ast.Name) and target.id == "dataclass_class":
            return decorator
        if isinstance(target, ast.Attribute) and target.attr == "dataclass_class":
            return decorator
    return None


def check_is_dataclass(ast_node: ast.ClassDef) -> bool:
    return retrieve_dataclass_decorator(ast_node) is not None


class COP008Check(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def visit_ClassDef(self, ast_node: ast.ClassDef) -> None:
        self._check_final_decorator(ast_node)
        self.generic_visit(ast_node)

    def _check_final_decorator(self, ast_node: ast.ClassDef) -> None:
        if (
            not check_is_dataclass(ast_node)
            and not contains_final_decorator(ast_node)
            and not ast_node.name.startswith("Test")
            and not inherits_from_whitelisted_class(ast_node)
        ):
            self.violations.append(Violation(ast_node.lineno, ast_node.col_offset, ViolationCode.FINAL_CLASS))
