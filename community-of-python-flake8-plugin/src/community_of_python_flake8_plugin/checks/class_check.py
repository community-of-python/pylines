from __future__ import annotations

import ast

from community_of_python_flake8_plugin.constants import FINAL_CLASS_EXCLUDED_BASES, MIN_NAME_LENGTH
from community_of_python_flake8_plugin.violations import Violation


def is_ignored_name(name: str) -> bool:
    if name == "_":
        return True
    if name.isupper():
        return True
    if name in {"value", "values", "pattern"}:
        return True
    if name.startswith("__") and name.endswith("__"):
        return True
    if name.startswith("_"):
        return True
    return False


def check_name_length(name: str, node: ast.AST) -> list[Violation]:
    if is_ignored_name(name):
        return []
    if len(name) < MIN_NAME_LENGTH:
        return [Violation(node.lineno, node.col_offset, "COP005 Name must be at least 8 characters")]
    return []


def is_true_literal(node: ast.AST | None) -> bool:
    return isinstance(node, ast.Constant) and node.value is True


def has_final_decorator(node: ast.ClassDef) -> bool:
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if isinstance(target, ast.Name) and target.id == "final":
            return True
        if isinstance(target, ast.Attribute) and target.attr == "final":
            return True
    return False


def inherits_from_whitelisted_class(node: ast.ClassDef) -> bool:
    for base in node.bases:
        if isinstance(base, ast.Name) and base.id in FINAL_CLASS_EXCLUDED_BASES:
            return True
        if isinstance(base, ast.Attribute) and base.attr in FINAL_CLASS_EXCLUDED_BASES:
            return True
    return False


def get_dataclass_decorator(node: ast.ClassDef) -> ast.expr | None:
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Call):
            target = decorator.func
        else:
            target = decorator
        if isinstance(target, ast.Name) and target.id == "dataclass":
            return decorator
        if isinstance(target, ast.Attribute) and target.attr == "dataclass":
            return decorator
    return None


def is_dataclass(node: ast.ClassDef) -> bool:
    return get_dataclass_decorator(node) is not None


def is_exception_class(node: ast.ClassDef) -> bool:
    return False


def check_class_name_length(node: ast.ClassDef) -> list[Violation]:
    if node.name.startswith("Test"):
        return []
    return check_name_length(node.name, node)


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
    if require_frozen and not is_true_literal(keywords.get("frozen")):
        return False
    return True


class ClassCheck(ast.NodeVisitor):
    def __init__(self) -> None:
        self.violations: list[Violation] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.violations.extend(check_class_name_length(node))
        self._check_final_decorator(node)
        self._check_dataclass_config(node)
        self.generic_visit(node)

    def _check_final_decorator(self, node: ast.ClassDef) -> None:
        if (
            not is_dataclass(node)
            and not has_final_decorator(node)
            and not node.name.startswith("Test")
            and not inherits_from_whitelisted_class(node)
        ):
            self.violations.append(Violation(node.lineno, node.col_offset, "COP010 Classes should be marked typing.final"))

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
                Violation(node.lineno, node.col_offset, "COP012 Use dataclasses with kw_only=True, slots=True, frozen=True")
            )
