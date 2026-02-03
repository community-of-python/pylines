from __future__ import annotations

import ast

from community_of_python_flake8_plugin.helpers import extract_safe_names
from community_of_python_flake8_plugin.violations import Violation


class SafeIndexVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []
        self._safe_name_stack: list[set[str]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for statement in node.body:
            self.visit(statement)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        for statement in node.body:
            self.visit(statement)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.value is not None:
            self.visit(node.value)

    def visit_If(self, node: ast.If) -> None:
        safe_names = extract_safe_names(node.test)
        if safe_names:
            self._safe_name_stack.append(safe_names)
            for statement in node.body:
                self.visit(statement)
            self._safe_name_stack.pop()
            for statement in node.orelse:
                self.visit(statement)
        else:
            self.generic_visit(node)

    def visit_Subscript(self, node: ast.Subscript) -> None:
        if isinstance(node.ctx, ast.Load) and isinstance(node.value, ast.Name):
            if not self._is_safe(node.value.id):
                self.violations.append(
                    Violation(node.lineno, node.col_offset, "COP004 Guard index/key access before subscripting")
                )
        self.generic_visit(node)

    def _is_safe(self, name: str) -> bool:
        return any(name in safe_names for safe_names in self._safe_name_stack)


def check_safe_index(node: ast.AST) -> list[Violation]:
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return []
    visitor = SafeIndexVisitor()
    visitor.visit(node)
    return visitor.violations
