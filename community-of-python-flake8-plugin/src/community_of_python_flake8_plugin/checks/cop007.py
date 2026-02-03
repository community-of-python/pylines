from __future__ import annotations
import ast
import typing

from community_of_python_flake8_plugin.violation_codes import ViolationCode
from community_of_python_flake8_plugin.violations import Violation


def collect_assignments(node: ast.AST) -> dict[str, list[ast.AST]]:
    assigned: typing.Final[dict[str, list[ast.AST]]] = {}
    for child in ast.walk(node):
        if isinstance(child, ast.Assign):
            for target in child.targets:
                if isinstance(target, ast.Name):
                    assigned.setdefault(target.id, []).append(child)
        if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
            assigned.setdefault(child.target.id, []).append(child)
    return assigned


def collect_load_counts(node: ast.AST) -> dict[str, int]:
    counts: typing.Final[dict[str, int]] = {}
    for child in ast.walk(node):
        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
            counts[child.id] = counts.get(child.id, 0) + 1
    return counts


class COP007Check(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_temporary_variables(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._check_temporary_variables(node)
        self.generic_visit(node)

    def _check_temporary_variables(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        assigned: typing.Final = collect_assignments(node)
        load_counts: typing.Final = collect_load_counts(node)
        for statement in node.body:
            if isinstance(statement, ast.Return) and isinstance(statement.value, ast.Name):
                name = statement.value.id
                if len(assigned.get(name, [])) == 1 and load_counts.get(name, 0) == 1:
                    self.violations.append(
                        Violation(statement.lineno, statement.col_offset, ViolationCode.TEMPORARY_VARIABLE)
                    )
