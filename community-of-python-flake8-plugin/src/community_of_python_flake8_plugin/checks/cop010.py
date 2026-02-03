from __future__ import annotations
import ast

from community_of_python_flake8_plugin.violation_codes import ViolationCode
from community_of_python_flake8_plugin.violations import Violation


def is_true_literal(node: ast.AST | None) -> bool:
    return isinstance(node, ast.Constant) and node.value is True


def get_dataclass_decorator(node: ast.ClassDef) -> ast.expr | None:
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if isinstance(target, ast.Name) and target.id == "dataclass":
            return decorator
        if isinstance(target, ast.Attribute) and target.attr == "dataclass":
            return decorator
    return None


def is_dataclass(node: ast.ClassDef) -> bool:
    return get_dataclass_decorator(node) is not None


def is_exception_class(_node: ast.ClassDef) -> bool:
    return False


def is_inheriting(node: ast.ClassDef) -> bool:
    return len(node.bases) > 0


def dataclass_has_keyword(decorator: ast.expr, name: str, value: bool | None = None) -> bool:
    if not isinstance(decorator, ast.Call):
        return False
    for keyword in decorator.keywords:
        if keyword.arg != name:
            continue
        if value is None:
            return True
        return isinstance(keyword.value, ast.Constant) and keyword.value.value is value
    return False


def dataclass_has_required_args(decorator: ast.expr, *, require_slots: bool, require_frozen: bool) -> bool:
    if not isinstance(decorator, ast.Call):
        return False
    keywords = {keyword.arg: keyword.value for keyword in decorator.keywords if keyword.arg}
    if not is_true_literal(keywords.get("kw_only")):
        return False
    if require_slots and not is_true_literal(keywords.get("slots")):
        return False
    return not (require_frozen and not is_true_literal(keywords.get("frozen")))


class COP010Check(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._check_dataclass_config(node)
        self.generic_visit(node)

    def _check_dataclass_config(self, node: ast.ClassDef) -> None:
        if not is_dataclass(node):
            return
        decorator = get_dataclass_decorator(node)
        if decorator is None:
            return
        if is_inheriting(node):
            return
        require_slots = not dataclass_has_keyword(decorator, "init", value=False)
        require_frozen = require_slots and not is_exception_class(node)
        if not dataclass_has_required_args(decorator, require_slots=require_slots, require_frozen=require_frozen):
            self.violations.append(
                Violation(node.lineno, node.col_offset, ViolationCode.DATACLASS_CONFIG)
            )
