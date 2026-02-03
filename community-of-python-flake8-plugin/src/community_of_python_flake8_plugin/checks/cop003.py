from __future__ import annotations
import ast

from community_of_python_flake8_plugin.constants import SCALAR_ANNOTATIONS
from community_of_python_flake8_plugin.violation_codes import ViolationCode
from community_of_python_flake8_plugin.violations import Violation


def is_literal_value(value: ast.AST) -> bool:
    if isinstance(value, ast.Constant):
        return True
    return bool(isinstance(value, (ast.List, ast.Tuple, ast.Set, ast.Dict)))


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


class COP003Check(ast.NodeVisitor):
    def __init__(self, tree: ast.AST) -> None:
        self.tree = tree
        self.violations: list[Violation] = []

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if isinstance(node.target, ast.Name):
            parent_class = get_parent_class(self.tree, node)
            parent_function = get_parent_function(self.tree, node)
            in_class_body = parent_class is not None and parent_function is None

            if not in_class_body:
                self._check_scalar_annotation(node)
        self.generic_visit(node)

    def _check_scalar_annotation(self, node: ast.AnnAssign) -> None:
        if node.value is None:
            return
        if not is_literal_value(node.value):
            return
        if is_scalar_annotation(node.annotation):
            self.violations.append(Violation(node.lineno, node.col_offset, ViolationCode.SCALAR_ANNOTATION))
