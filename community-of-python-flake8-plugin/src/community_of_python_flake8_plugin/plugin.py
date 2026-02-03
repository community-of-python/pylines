from __future__ import annotations
import typing
from typing import TYPE_CHECKING, Final


if TYPE_CHECKING:
    import ast
    from collections.abc import Iterable

from community_of_python_flake8_plugin.checks import execute_all_validations


@typing.final
class CommunityOfPythonFlake8Plugin:
    name = "community-of-python-flake8-plugin"
    version = "0.1.27"

    def __init__(self, tree: ast.AST) -> None:
        self.tree = tree

    def run(self) -> Iterable[tuple[int, int, str, type[object]]]:
        violations: Final = execute_all_validations(self.tree)
        for violation in violations:
            code_info = violation.code.value
            message = f"{code_info['code']} {code_info['description']}"
            yield violation.line, violation.col, message, type(self)
