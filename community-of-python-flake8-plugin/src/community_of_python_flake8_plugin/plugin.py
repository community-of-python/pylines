from __future__ import annotations

import ast
from typing import Iterable

from community_of_python_flake8_plugin.checks.annotations import check_attribute_annotation, check_scalar_annotation
from community_of_python_flake8_plugin.checks.immutability import check_class_definition, check_module_assignments
from community_of_python_flake8_plugin.checks.imports import check_import_from
from community_of_python_flake8_plugin.helpers import module_has_all
from community_of_python_flake8_plugin.checks.naming import (
    check_attribute_name_length,
    check_function_verb,
    check_get_prefix,
    check_name_length,
)
from community_of_python_flake8_plugin.checks.temporary_vars import check_temporary_variables
from community_of_python_flake8_plugin.violations import Violation


class CommunityOfPythonFlake8Plugin:
    name = "community-of-python-flake8-plugin"
    version = "0.1.27"

    def __init__(self, tree: ast.AST):
        self.tree = tree

    def run(self) -> Iterable[tuple[int, int, str, type[object]]]:
        checker = _Checker()
        checker.visit(self.tree)
        for violation in checker.violations:
            yield violation.line, violation.col, violation.message, type(self)


class _Checker(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []
        self._function_depth = 0
        self._class_depth = 0
        self._module_has_all = False

    def visit_Module(self, node: ast.Module) -> None:
        self._module_has_all = module_has_all(node)
        self.violations.extend(check_module_assignments(node))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.violations.extend(check_import_from(node, self._module_has_all))
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if self._function_depth > 0 and isinstance(node.target, ast.Name):
            self.violations.extend(check_name_length(node.target.id, node))
        if self._function_depth > 0:
            self.violations.extend(check_attribute_name_length(node))
        in_class_body = self._class_depth > 0 and self._function_depth == 0
        self.violations.extend(check_scalar_annotation(node, in_class_body))
        self.violations.extend(check_attribute_annotation(node))
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        if self._function_depth > 0:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.violations.extend(check_name_length(target.id, node))
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._check_function(node)
        self._function_depth += 1
        self.generic_visit(node)
        self._function_depth -= 1

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._check_function(node)
        self._function_depth += 1
        self.generic_visit(node)
        self._function_depth -= 1

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.violations.extend(check_class_definition(node))
        self._class_depth += 1
        self.generic_visit(node)
        self._class_depth -= 1

    def _check_function(self, node: ast.AST) -> None:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            self.violations.extend(check_name_length(node.name, node))
            self.violations.extend(check_get_prefix(node))
            self.violations.extend(check_function_verb(node))
            self.violations.extend(check_temporary_variables(node))
