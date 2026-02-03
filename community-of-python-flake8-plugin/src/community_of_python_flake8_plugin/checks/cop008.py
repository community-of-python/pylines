from __future__ import annotations
import ast

from community_of_python_flake8_plugin.constants import FINAL_CLASS_EXCLUDED_BASES
from community_of_python_flake8_plugin.violation_codes import ViolationCode
from community_of_python_flake8_plugin.violations import Violation


def is_true_literal(node: ast.AST | None) -> bool:
    return isinstance(node, ast.Constant) and node.value is True


def has_final_decorator(node: ast.ClassDef) -> bool:
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if isinstance(target, ast.Name) and target.id == "final":
            return True
        if isinstance(target, ast.Attribute) and target.attr == "final":
            return True
    return False


def inherits_from_whitelisted_class(node: ast.ClassDef) -> bool:
    for base in node.bases:
        if isinstance(base, ast.Name) and base.id in FINAL_CLASS_EXCLUDED_BASES:
            return True
        if isinstance(base, ast.Attribute) and base.attr in FINAL_CLASS_EXCLUDED_BASES:
            return True
    return False


def get_dataclass_decorator(node: ast.ClassDef) -> ast.expr | None:
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if isinstance(target, ast.Name) and target.id == "dataclass":
            return decorator
        if isinstance(target, ast.Attribute) and target.attr == "dataclass":
            return decorator
    return None


def is_dataclass(node: ast.ClassDef) -> bool:
    return get_dataclass_decorator(node) is not None


class COP008Check(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._check_final_decorator(node)
        self.generic_visit(node)

    def _check_final_decorator(self, node: ast.ClassDef) -> None:
        if (
            not is_dataclass(node)
            and not has_final_decorator(node)
            and not node.name.startswith("Test")
            and not inherits_from_whitelisted_class(node)
        ):
            self.violations.append(Violation(node.lineno, node.col_offset, ViolationCode.FINAL_CLASS))
