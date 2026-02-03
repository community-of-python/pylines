from __future__ import annotations

import ast
import importlib.util
import sys

from community_of_python_flake8_plugin.constants import MAPPING_PROXY_TYPES, SCALAR_ANNOTATIONS, VERB_PREFIXES


def collect_assignments(node: ast.AST) -> dict[str, list[ast.AST]]:
    assigned: dict[str, list[ast.AST]] = {}
    for child in ast.walk(node):
        if isinstance(child, ast.Assign):
            for target in child.targets:
                if isinstance(target, ast.Name):
                    assigned.setdefault(target.id, []).append(child)
        if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
            assigned.setdefault(child.target.id, []).append(child)
    return assigned


def collect_load_counts(node: ast.AST) -> dict[str, int]:
    counts: dict[str, int] = {}
    for child in ast.walk(node):
        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
            counts[child.id] = counts.get(child.id, 0) + 1
    return counts


def module_has_all(node: ast.Module) -> bool:
    for statement in node.body:
        if isinstance(statement, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "__all__" for target in statement.targets):
                return True
        if isinstance(statement, ast.AnnAssign):
            if isinstance(statement.target, ast.Name) and statement.target.id == "__all__":
                return True
    return False


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


def is_verb_name(name: str) -> bool:
    return any(name == verb or name.startswith(f"{verb}_") for verb in VERB_PREFIXES)


def is_property(node: ast.AST) -> bool:
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    return any(is_property_decorator(decorator) for decorator in node.decorator_list)


def is_pytest_fixture(node: ast.AST) -> bool:
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    return any(is_fixture_decorator(decorator) for decorator in node.decorator_list)


def is_property_decorator(decorator: ast.expr) -> bool:
    if isinstance(decorator, ast.Name):
        return decorator.id == "property"
    if isinstance(decorator, ast.Attribute):
        return decorator.attr.endswith("property") or decorator.attr == "setter"
    return False


def is_fixture_decorator(decorator: ast.expr) -> bool:
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Name):
        return target.id == "fixture"
    if isinstance(target, ast.Attribute):
        return target.attr == "fixture" and isinstance(target.value, ast.Name) and target.value.id == "pytest"
    return False


def is_stdlib_module(module_name: str) -> bool:
    return module_name in sys.stdlib_module_names


def is_stdlib_package(module_name: str) -> bool:
    if not is_stdlib_module(module_name):
        return False
    spec = importlib.util.find_spec(module_name)
    return spec is not None and spec.submodule_search_locations is not None


def is_scalar_annotation(annotation: ast.AST) -> bool:
    if isinstance(annotation, ast.Name):
        return annotation.id in SCALAR_ANNOTATIONS
    if isinstance(annotation, ast.Attribute):
        return annotation.attr in SCALAR_ANNOTATIONS
    if isinstance(annotation, ast.Subscript):
        return is_scalar_annotation(annotation.value) or is_final_annotation(annotation.value)
    return False


def is_literal_value(value: ast.AST) -> bool:
    if isinstance(value, ast.Constant):
        return True
    if isinstance(value, (ast.List, ast.Tuple, ast.Set, ast.Dict)):
        return True
    return False


def is_final_annotation(annotation: ast.AST) -> bool:
    if isinstance(annotation, ast.Name):
        return annotation.id == "Final"
    if isinstance(annotation, ast.Attribute):
        return annotation.attr == "Final"
    if isinstance(annotation, ast.Subscript):
        return is_final_annotation(annotation.value)
    return False


def is_mapping_literal(value: ast.AST | None) -> bool:
    if isinstance(value, ast.Dict):
        return True
    if isinstance(value, ast.Call):
        return any(isinstance(arg, ast.Dict) for arg in value.args)
    return False


def is_mapping_proxy_call(value: ast.AST | None) -> bool:
    if not isinstance(value, ast.Call):
        return False
    if isinstance(value.func, ast.Name):
        return value.func.id in MAPPING_PROXY_TYPES
    if isinstance(value.func, ast.Attribute):
        return value.func.attr in MAPPING_PROXY_TYPES
    return False


def is_dataclass(node: ast.ClassDef) -> bool:
    return get_dataclass_decorator(node) is not None


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


def dataclass_has_required_args(decorator: ast.expr) -> bool:
    if isinstance(decorator, ast.Call):
        keywords = {keyword.arg: keyword.value for keyword in decorator.keywords if keyword.arg}
        return (
            is_true_literal(keywords.get("kw_only"))
            and is_true_literal(keywords.get("slots"))
            and is_true_literal(keywords.get("frozen"))
        )
    return False


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


def should_be_dataclass(node: ast.ClassDef) -> bool:
    if has_final_decorator(node):
        return False
    return any(isinstance(statement, ast.FunctionDef) and statement.name == "__init__" for statement in node.body)
