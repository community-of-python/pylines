from __future__ import annotations

import ast
from typing import Iterable

from community_of_python_flake8_plugin.checks import run_all_checks


class CommunityOfPythonFlake8Plugin:
    name = "community-of-python-flake8-plugin"
    version = "0.1.27"

    def __init__(self, tree: ast.AST):
        self.tree = tree

    def run(self) -> Iterable[tuple[int, int, str, type[object]]]:
        violations = run_all_checks(self.tree)
        for violation in violations:
            yield violation.line, violation.col, violation.message, type(self)
