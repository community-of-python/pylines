from __future__ import annotations
import ast
import typing

from community_of_python_flake8_plugin.violation_codes import ViolationCode
from community_of_python_flake8_plugin.violations import Violation


def collect_assignments(ast_node: ast.AST) -> dict[str, list[ast.AST]]:
    assigned: typing.Final[dict[str, list[ast.AST]]] = {}
    for child in ast.walk(ast_node):
        if isinstance(child, ast.Assign):
            for target in child.targets:
                if isinstance(target, ast.Name):
                    assigned.setdefault(target.id, []).append(child)
        if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
            assigned.setdefault(child.target.id, []).append(child)
    return assigned


def collect_load_counts(ast_node: ast.AST) -> dict[str, int]:
    counts: typing.Final[dict[str, int]] = {}
    for child in ast.walk(ast_node):
        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
            counts[child.id] = counts.get(child.id, 0) + 1
    return counts


class COP007Check(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def visit_FunctionDef(self, ast_node: ast.FunctionDef) -> None:
        self._check_temporary_variables(ast_node)
        self.generic_visit(ast_node)

    def visit_AsyncFunctionDef(self, ast_node: ast.AsyncFunctionDef) -> None:
        self._check_temporary_variables(ast_node)
        self.generic_visit(ast_node)

    def _check_temporary_variables(self, ast_node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        assigned: typing.Final = collect_assignments(ast_node)
        load_counts: typing.Final = collect_load_counts(ast_node)
        for statement in ast_node.body:
            if isinstance(statement, ast.Return) and isinstance(statement.value, ast.Name):
                identifier = statement.value.id
                if len(assigned.get(identifier, [])) == 1 and load_counts.get(identifier, 0) == 1:
                    self.violations.append(
                        Violation(statement.lineno, statement.col_offset, ViolationCode.TEMPORARY_VARIABLE)
                    )
