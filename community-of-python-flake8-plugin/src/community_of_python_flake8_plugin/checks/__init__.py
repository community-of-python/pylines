from __future__ import annotations
import ast
import typing
from typing import TYPE_CHECKING

from community_of_python_flake8_plugin.checks.cop001 import COP001Check
from community_of_python_flake8_plugin.checks.cop002 import COP002Check
from community_of_python_flake8_plugin.checks.cop003 import COP003Check
from community_of_python_flake8_plugin.checks.cop004 import COP004Check
from community_of_python_flake8_plugin.checks.cop005 import COP005Check
from community_of_python_flake8_plugin.checks.cop006 import COP006Check
from community_of_python_flake8_plugin.checks.cop007 import COP007Check
from community_of_python_flake8_plugin.checks.cop008 import COP008Check
from community_of_python_flake8_plugin.checks.cop009 import COP009Check
from community_of_python_flake8_plugin.checks.cop010 import COP010Check


if TYPE_CHECKING:
    from community_of_python_flake8_plugin.violations import Violation


def module_has_all(node: ast.Module) -> bool:
    for statement in node.body:
        if isinstance(statement, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "__all__" for target in statement.targets
        ):
            return True
        if (
            isinstance(statement, ast.AnnAssign)
            and isinstance(statement.target, ast.Name)
            and statement.target.id == "__all__"
        ):
            return True
    return False


def get_parent_class(tree: ast.AST, node: ast.AST) -> ast.ClassDef | None:
    for potential_parent in ast.walk(tree):
        if isinstance(potential_parent, ast.ClassDef):
            for child in ast.walk(potential_parent):
                if child is node:
                    return potential_parent
    return None


def run_all_checks(tree: ast.AST) -> list[Violation]:
    has_all: typing.Final = module_has_all(tree)
    all_violations: typing.Final[list[Violation]] = []

    # COP001: Use module import when importing more than two names
    cop001_check: typing.Final = COP001Check(has_all)
    cop001_check.visit(tree)
    all_violations.extend(cop001_check.violations)

    # COP002: Import standard library modules as whole modules
    cop002_check: typing.Final = COP002Check()
    cop002_check.visit(tree)
    all_violations.extend(cop002_check.violations)

    # COP003: Avoid explicit scalar type annotations
    cop003_check: typing.Final = COP003Check(tree)
    cop003_check.visit(tree)
    all_violations.extend(cop003_check.violations)

    # COP004: Name must be at least 8 characters
    cop004_check: typing.Final = COP004Check(tree)
    cop004_check.visit(tree)
    all_violations.extend(cop004_check.violations)

    # COP005: Function name must be a verb
    cop005_check: typing.Final = COP005Check(tree)
    cop005_check.visit(tree)
    all_violations.extend(cop005_check.violations)

    # COP006: Avoid get_ prefix in async function names
    cop006_check: typing.Final = COP006Check()
    cop006_check.visit(tree)
    all_violations.extend(cop006_check.violations)

    # COP007: Avoid temporary variables used only once
    cop007_check: typing.Final = COP007Check()
    cop007_check.visit(tree)
    all_violations.extend(cop007_check.violations)

    # COP008: Classes should be marked typing.final
    cop008_check: typing.Final = COP008Check()
    cop008_check.visit(tree)
    all_violations.extend(cop008_check.violations)

    # COP009: Wrap module dictionaries with types.MappingProxyType
    cop009_check: typing.Final = COP009Check()
    cop009_check.visit(tree)
    all_violations.extend(cop009_check.violations)

    # COP010: Use dataclasses with kw_only=True, slots=True, frozen=True
    cop010_check: typing.Final = COP010Check()
    cop010_check.visit(tree)
    all_violations.extend(cop010_check.violations)

    return all_violations
