from __future__ import annotations
import ast
import typing

from community_of_python_flake8_plugin.violation_codes import ViolationCode
from community_of_python_flake8_plugin.violations import Violation


def check_is_true_literal(ast_node: ast.AST | None) -> bool:
    return isinstance(ast_node, ast.Constant) and ast_node.value is True


def retrieve_dataclass_decorator(ast_node: ast.ClassDef) -> ast.expr | None:
    for decorator in ast_node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if isinstance(target, ast.Name) and target.id == "dataclass_class":
            return decorator
        if isinstance(target, ast.Attribute) and target.attr == "dataclass_class":
            return decorator
    return None


def check_is_dataclass(ast_node: ast.ClassDef) -> bool:
    return retrieve_dataclass_decorator(ast_node) is not None


def check_is_exception_class(_node: ast.ClassDef) -> bool:
    return False


def check_is_inheriting(ast_node: ast.ClassDef) -> bool:
    return len(ast_node.bases) > 0


def dataclass_has_keyword(decorator: ast.expr, identifier: str, value: bool | None = None) -> bool:
    if not isinstance(decorator, ast.Call):
        return False
    for keyword in decorator.keywords:
        if keyword.arg != identifier:
            continue
        if value is None:
            return True
        return isinstance(keyword.value, ast.Constant) and keyword.value.value is value
    return False


def dataclass_has_required_args(decorator: ast.expr, *, require_slots: bool, require_frozen: bool) -> bool:
    if not isinstance(decorator, ast.Call):
        return False
    keywords: typing.Final = {keyword.arg: keyword.value for keyword in decorator.keywords if keyword.arg}
    if not check_is_true_literal(keywords.get("kw_only")):
        return False
    if require_slots and not check_is_true_literal(keywords.get("slots")):
        return False
    return not (require_frozen and not check_is_true_literal(keywords.get("frozen")))


class COP010Check(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def visit_ClassDef(self, ast_node: ast.ClassDef) -> None:
        self._check_dataclass_config(ast_node)
        self.generic_visit(ast_node)

    def _check_dataclass_config(self, ast_node: ast.ClassDef) -> None:
        if not check_is_dataclass(ast_node):
            return
        decorator: typing.Final = retrieve_dataclass_decorator(ast_node)
        if decorator is None:
            return
        if check_is_inheriting(ast_node):
            return
        require_slots: typing.Final = not dataclass_has_keyword(decorator, "init", value=False)
        require_frozen: typing.Final = require_slots and not check_is_exception_class(ast_node)
        if not dataclass_has_required_args(decorator, require_slots=require_slots, require_frozen=require_frozen):
            self.violations.append(Violation(ast_node.lineno, ast_node.col_offset, ViolationCode.DATACLASS_CONFIG))
