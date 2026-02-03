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
from community_of_python_flake8_plugin.utils import check_module_has_all_declaration


if TYPE_CHECKING:
    import ast

    from community_of_python_flake8_plugin.violations import Violation


def execute_all_validations(syntax_tree: ast.AST) -> list[Violation]:
    contains_all_declaration: typing.Final = check_module_has_all_declaration(syntax_tree)
    collected_violations: typing.Final[list[Violation]] = []

    # COP001: Use module import when importing more than two names
    cop001_validator: typing.Final = COP001Check(contains_all_declaration)
    cop001_validator.visit(syntax_tree)
    collected_violations.extend(cop001_validator.violations)

    # COP002: Import standard library modules as whole modules
    cop002_validator: typing.Final = COP002Check()
    cop002_validator.visit(syntax_tree)
    collected_violations.extend(cop002_validator.violations)

    # COP003: Avoid explicit scalar type annotations
    cop003_validator: typing.Final = COP003Check(syntax_tree)
    cop003_validator.visit(syntax_tree)
    collected_violations.extend(cop003_validator.violations)

    # COP004: Name must be at least 8 characters
    cop004_validator: typing.Final = COP004Check(syntax_tree)
    cop004_validator.visit(syntax_tree)
    collected_violations.extend(cop004_validator.violations)

    # COP005: Function identifier must be a verb
    cop005_validator: typing.Final = COP005Check(syntax_tree)
    cop005_validator.visit(syntax_tree)
    collected_violations.extend(cop005_validator.violations)

    # COP006: Avoid get_ prefix in async function names
    cop006_validator: typing.Final = COP006Check()
    cop006_validator.visit(syntax_tree)
    collected_violations.extend(cop006_validator.violations)

    # COP007: Avoid temporary variables used only once
    cop007_validator: typing.Final = COP007Check()
    cop007_validator.visit(syntax_tree)
    collected_violations.extend(cop007_validator.violations)

    # COP008: Classes should be marked typing.final
    cop008_validator: typing.Final = COP008Check()
    cop008_validator.visit(syntax_tree)
    collected_violations.extend(cop008_validator.violations)

    # COP009: Wrap module dictionaries with types.MappingProxyType
    cop009_validator: typing.Final = COP009Check()
    cop009_validator.visit(syntax_tree)
    collected_violations.extend(cop009_validator.violations)

    # COP010: Use dataclasses with kw_only=True, slots=True, frozen=True
    cop010_validator: typing.Final = COP010Check()
    cop010_validator.visit(syntax_tree)
    collected_violations.extend(cop010_validator.violations)

    return collected_violations
