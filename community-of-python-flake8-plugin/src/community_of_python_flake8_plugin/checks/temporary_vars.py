from __future__ import annotations

import ast

from community_of_python_flake8_plugin.helpers import collect_assignments, collect_load_counts
from community_of_python_flake8_plugin.violations import Violation


def check_temporary_variables(node: ast.AST) -> list[Violation]:
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return []
    assigned = collect_assignments(node)
    load_counts = collect_load_counts(node)
    for statement in node.body:
        if isinstance(statement, ast.Return) and isinstance(statement.value, ast.Name):
            name = statement.value.id
            if len(assigned.get(name, [])) == 1 and load_counts.get(name, 0) == 1:
                return [Violation(statement.lineno, statement.col_offset, "COP008 Avoid temporary variables used only once")]
    return []
