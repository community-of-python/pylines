from __future__ import annotations

import ast

from community_of_python_flake8_plugin.constants import MIN_NAME_LENGTH, SCALAR_ANNOTATIONS
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


def is_literal_value(value: ast.AST) -> bool:
    if isinstance(value, ast.Constant):
        return True
    if isinstance(value, (ast.List, ast.Tuple, ast.Set, ast.Dict)):
        return True
    return False


def is_final_annotation(annotation: ast.AST) -> bool:
    if isinstance(annotation, ast.Name):
        return annotation.id == "Final"
    if isinstance(annotation, ast.Attribute):
        return annotation.attr == "Final"
    if isinstance(annotation, ast.Subscript):
        return is_final_annotation(annotation.value)
    return False


def is_scalar_annotation(annotation: ast.AST) -> bool:
    if isinstance(annotation, ast.Name):
        return annotation.id in SCALAR_ANNOTATIONS
    if isinstance(annotation, ast.Attribute):
        return annotation.attr in SCALAR_ANNOTATIONS
    if isinstance(annotation, ast.Subscript):
        if is_final_annotation(annotation.value):
            return is_scalar_annotation(annotation.slice)
        return is_scalar_annotation(annotation.value)
    return False


class AnnotationCheck(ast.NodeVisitor):
    def __init__(self, in_class_body: bool = False) -> None:
        self.in_class_body = in_class_body
        self.violations: list[Violation] = []

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if isinstance(node.target, ast.Name):
            if self.in_class_body:
                self._check_name_length(node.target.id, node)
            self._check_scalar_annotation(node)
        self.generic_visit(node)

    def _check_name_length(self, name: str, node: ast.AST) -> None:
        if is_ignored_name(name):
            return
        if len(name) < MIN_NAME_LENGTH:
            self.violations.append(Violation(node.lineno, node.col_offset, "COP005 Name must be at least 8 characters"))

    def _check_scalar_annotation(self, node: ast.AnnAssign) -> None:
        if node.value is None:
            return
        if self.in_class_body:
            return
        if not is_literal_value(node.value):
            return
        if is_scalar_annotation(node.annotation):
            self.violations.append(
                Violation(node.lineno, node.col_offset, "COP003 Avoid explicit scalar type annotations")
            )
