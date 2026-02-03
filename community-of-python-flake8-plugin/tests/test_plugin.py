from __future__ import annotations
import ast

import pytest
from community_of_python_flake8_plugin.plugin import CommunityOfPythonFlake8Plugin


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        # COP001: Use module import when importing more than two names
        ("from x import a, b, c", ["COP001"]),
        # COP002: Import standard library modules as whole modules
        ("from os import name", ["COP002"]),
        # No violation: unittest mock is allowed
        ("from unittest import mock", []),
        # No violation: importlib resources submodules are allowed
        ("from importlib import resources", []),
        ("from importlib import metadata", []),
        # COP002: Even resources submodule should be imported as whole
        ("from importlib.resources import files", ["COP002"]),
        # No violation: __future__ imports are allowed
        ("from __future__ import annotations", []),
        # No violation: third-party imports are fine
        ("from third_party import widget", []),
        # COP001: Importing more than two names from third party
        ("from my_project.settings import A, B, C", []),
        # No violation: collections.abc is whitelisted
        ("from collections.abc import AsyncIterator", []),
        # No violation: Multiple imports from stdlib subpackage
        ("from importlib import resources, simple, util", []),
        # No violation: When __all__ is defined, more than two imports are allowed
        ("__all__ = ['a', 'b', 'c']\nfrom x import a, b, c", []),
        # COP003: Avoid explicit scalar type annotations with literal values
        ("value: str = 'hello'", ["COP003"]),
        # No violation: Scalar annotation is fine with non-literal value
        ("value: int = do_something()", []),
        # COP003: Even with Final, scalar annotation with literal is flagged
        ("value: typing.Final[int] = 1", ["COP003"]),
        # Note: self.value annotations are in method bodies, not class bodies, so no violation
        ("self.value: str = 'hello'", []),
        # COP004: Argument name too short (user) - fetch_item is a valid verb (starts with "fetch")
        ("def fetch_item(user: int) -> int:\n    return user", ["COP004"]),
        # COP004: Argument name too short (user) - fetch_item is a valid verb
        ("def fetch_item(self, user: int) -> int:\n    return user", ["COP004"]),
        ("def fetch_item(cls, user: int) -> int:\n    return user", ["COP004"]),
        # COP004: Argument name too short - fetch_item is a valid verb
        ("def fetch_item(*args: int) -> int:\n    return 1", ["COP004"]),
        ("def fetch_item(**kwargs: int) -> int:\n    return 1", ["COP004"]),
        # COP004, COP008: Class name too short and not marked final
        ("class Abc:\n    value: int = 1", ["COP004", "COP008"]),
        # COP004, COP008: Single-letter class name and not marked final
        ("class C:\n    a: int = 1", ["COP004", "COP008"]),
        # No violation: Test classes are exempt
        ("class TestExample:\n    value: int", []),
        # COP004: Function name must be a verb
        ("def total_value() -> int:\n    return 1", ["COP005"]),
        # No violation: get_ prefix is allowed for sync functions
        ("def get_user_data() -> str:\n    return 'value'", []),
        # COP005: Avoid get_ prefix in async function names
        ("async def get_user_data() -> str:\n    return 'value'", ["COP006"]),
        # No violation: Test functions are exempt
        ("def test_example() -> None:\n    return None", []),
        # No violation: main function is exempt
        ("def main() -> None:\n    return None", []),
        # No violation: pytest fixture is exempt from naming rules
        ("import pytest\n\n@pytest.fixture\ndef data():\n    return 1", []),
        # COP006: Avoid temporary variables used only once
        (
            "def fetch_value() -> int:\n    result_value = 1\n    another_value = result_value\n    return another_value",
            ["COP007"],
        ),
        # No violation: Variable used multiple times
        ("def fetch_item(values: list[int]) -> int:\n    return values[0]", []),
        # No violation: Variable used in conditional
        (
            "def fetch_item(values: list[int]) -> int | None:\n    if len(values) > 0:\n        return values[0]\n    return None",
            [],
        ),
        # COP004: Function name must be a verb (even with mutable params)
        ("def fill_values(values: list[int]) -> None:\n    values[0] = 1", ["COP005"]),
        # No violation: Uppercase constants are exempt
        ("VALUE = 10", []),
        # COP007: Classes should be marked typing.final
        (
            "class FinalClass:\n    value: int\n    def __init__(self, value: int) -> None:\n        self.value = value",
            ["COP008"],
        ),
        # No violation: Classes inheriting from BaseModel are exempt
        ("from pydantic import BaseModel\nclass MyBaseModel(BaseModel): ...", []),
        ("import pydantic\nclass MyBaseModel(pydantic.BaseModel): ...", []),
        # No violation: Classes inheriting from RootModel are exempt
        ("from pydantic import RootModel\nclass MyRootModel(RootModel): ...", []),
        # No violation: Classes inheriting from ModelFactory are exempt
        (
            "from polyfactory.factories.pydantic_factory import ModelFactory\nclass MyModelFactory(ModelFactory): ...",
            [],
        ),
        # COP004, COP010: Dataclass with short name and missing required args
        (
            "import dataclasses\n\n@dataclasses.dataclass\nclass Example:\n    value: int\n    name: str\n",
            ["COP004", "COP010", "COP004"],
        ),
        # COP004: Dataclass with correct config but short name
        (
            "import dataclasses\n\n"
            "@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)\n"
            "class Example:\n"
            "    value: int\n",
            ["COP004"],
        ),
        # COP004, COP010: Dataclass with init=False still needs slots and frozen
        (
            "import dataclasses\n\n@dataclasses.dataclass(init=False)\nclass Example:\n    value: int\n",
            ["COP004", "COP010"],
        ),
        # No violation: Exception classes don't need frozen
        (
            "import dataclasses\n\n@dataclasses.dataclass\nclass ExampleError(ValueError):\n    value: int\n",
            [],
        ),
        # No violation: Inheriting dataclasses don't need validation
        (
            "import dataclasses\n\n@dataclasses.dataclass\nclass ExampleChild(Example):\n    value: int\n",
            [],
        ),
        # COP009: Wrap module dictionaries with types.MappingProxyType
        ("values = {'key': 'value'}", ["COP009"]),
        # COP002: TypedDict should be imported from typing module, not via from import
        (
            "from typing import TypedDict, NotRequired\n\n"
            "UnsubscribeHeaders = TypedDict(\n"
            "    'UnsubscribeHeaders',\n"
            "    {\n"
            "        'id': str,\n"
            "        'content-length': NotRequired[str],\n"
            "    },\n"
            ")",
            ["COP002"],
        ),
        # No violation: TypedDict imported correctly from typing module
        (
            "import typing\n\n"
            "UnsubscribeHeaders = typing.TypedDict(\n"
            "    'UnsubscribeHeaders',\n"
            "    {\n"
            "        'id': str,\n"
            "        'content-length': typing.NotRequired[str],\n"
            "    },\n"
            ")",
            [],
        ),
        # No violation: Classes inheriting from ModelFactory are exempt
        (
            "from polyfactory.factories.pydantic_factory import ModelFactory\n"
            "class MyModelFactory(ModelFactory):\n"
            "    def fn():\n"
            "        pass",
            [],
        ),
        # No violation: Dictionary wrapped in MappingProxyType
        ("import types\nvalues = types.MappingProxyType({'key': 'value'})", []),
        # No violation: Simple integer assignment
        ("value = 1", []),
        # No violation: pytest fixture annotation is whitelisted
        (
            "import pytest\n@pytest.fixture\ndef some_fixture(arg: pytest.fixture): pass",
            [],
        ),
        # No violation: pytest fixture annotation (imported) is whitelisted
        (
            "from pytest import fixture\n@fixture\ndef some_fixture(arg: fixture): pass",
            [],
        ),
        # COP004: faker.Faker annotation doesn't exempt function naming rules
        (
            "import faker\ndef some_func(arg: faker.Faker): pass",
            ["COP005"],
        ),
        # COP004: Faker annotation doesn't exempt function naming rules
        (
            "from faker import Faker\ndef some_func(arg: Faker): pass",
            ["COP005"],
        ),
        # COP004, COP004, COP008: MyClass (short name), calc (short name), MyClass (not final)
        (
            "import functools\nclass MyClass:\n    @functools.cached_property\n    def calc(): pass",
            ["COP004", "COP004", "COP008"],
        ),
    ],
)
def test_plugin_reports(source: str, expected: list[str]) -> None:
    tree = ast.parse(source)
    messages = [item[2] for item in CommunityOfPythonFlake8Plugin(tree).run()]
    codes = [message.split(" ")[0] for message in messages]
    assert sorted(codes) == sorted(expected)
