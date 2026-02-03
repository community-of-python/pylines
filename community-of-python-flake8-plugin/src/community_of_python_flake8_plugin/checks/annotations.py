from __future__ import annotations

import ast

from community_of_python_flake8_plugin.helpers import is_final_annotation, is_scalar_annotation
from community_of_python_flake8_plugin.violations import Violation


def check_scalar_annotation(node: ast.AnnAssign, in_class_body: bool) -> list[Violation]:
    if node.value is None:
        return []
    if in_class_body:
        return []
    if is_scalar_annotation(node.annotation) and not is_final_annotation(node.annotation):
        return [Violation(node.lineno, node.col_offset, "COP003 Avoid explicit scalar type annotations")]
    return []


def check_attribute_annotation(node: ast.AnnAssign) -> list[Violation]:
    return []
