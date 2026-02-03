from __future__ import annotations

import ast

from community_of_python_flake8_plugin.helpers import (
    dataclass_has_required_args,
    get_dataclass_decorator,
    has_final_decorator,
    is_dataclass,
    is_mapping_literal,
    is_mapping_proxy_call,
)
from community_of_python_flake8_plugin.violations import Violation


def check_module_assignments(node: ast.Module) -> list[Violation]:
    violations: list[Violation] = []
    for statement in node.body:
        if isinstance(statement, ast.Assign):
            if is_mapping_literal(statement.value) and not is_mapping_proxy_call(statement.value):
                violations.append(
                    Violation(statement.lineno, statement.col_offset, "COP011 Wrap module dictionaries with types.MappingProxyType")
                )
        if isinstance(statement, ast.AnnAssign):
            if is_mapping_literal(statement.value) and not is_mapping_proxy_call(statement.value):
                violations.append(
                    Violation(statement.lineno, statement.col_offset, "COP011 Wrap module dictionaries with types.MappingProxyType")
                )
    return violations


def check_class_definition(node: ast.ClassDef) -> list[Violation]:
    violations: list[Violation] = []
    if not is_dataclass(node) and not has_final_decorator(node) and not node.name.startswith("Test"):
        violations.append(Violation(node.lineno, node.col_offset, "COP010 Classes should be marked typing.final"))
    if is_dataclass(node):
        decorator = get_dataclass_decorator(node)
        if decorator is not None and not dataclass_has_required_args(decorator):
            violations.append(
                Violation(node.lineno, node.col_offset, "COP012 Use dataclasses with kw_only=True, slots=True, frozen=True")
            )
    return violations
