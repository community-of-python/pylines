from __future__ import annotations
from typing import TYPE_CHECKING

from community_of_python_flake8_plugin.checks import run_all_checks

if TYPE_CHECKING:
    import ast
    from collections.abc import Iterable


class CommunityOfPythonFlake8Plugin:
    name = "community-of-python-flake8-plugin"
    version = "0.1.27"

    def __init__(self, tree: ast.AST) -> None:
        self.tree = tree

    def run(self) -> Iterable[tuple[int, int, str, type[object]]]:
        violations = run_all_checks(self.tree)
        for violation in violations:
            code_info = violation.code.value
            message = f"{code_info['code']} {code_info['description']}"
            yield violation.line, violation.col, message, type(self)
