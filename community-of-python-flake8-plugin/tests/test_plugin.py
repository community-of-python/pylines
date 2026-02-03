from __future__ import annotations

import ast

import pytest

from community_of_python_flake8_plugin.plugin import CommunityOfPythonFlake8Plugin


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("from os import name", ["COP002"]),
        ("from unittest import mock", []),
        ("from importlib import resources", []),
        ("from importlib import metadata", []),
        ("from importlib.resources import files", ["COP002"]),
        ("from __future__ import annotations", []),
        ("from third_party import widget", []),
        ("from x import a, b, c", ["COP001"]),
        ("from importlib import resources, simple, util", []),
        ("__all__ = ['a', 'b', 'c']\nfrom x import a, b, c", []),
        ("value: str = 'hello'", ["COP003"]),
        ("value: int = do_something()", []),
        ("value: typing.Final[int] = 1", ["COP003"]),
        ("self.value: str = 'hello'", ["COP003"]),
        ("def fetch_item(user: int) -> int:\n    return user", ["COP005"]),
        ("def fetch_item(self, user: int) -> int:\n    return user", ["COP005"]),
        ("def fetch_item(cls, user: int) -> int:\n    return user", ["COP005"]),
        ("def fetch_item(*args: int) -> int:\n    return 1", ["COP005"]),
        ("def fetch_item(**kwargs: int) -> int:\n    return 1", ["COP005"]),
        ("class Abc:\n    value: int = 1", ["COP005", "COP010"]),
        ("class C:\n    a: int = 1", ["COP005", "COP010"]),
        ("class TestExample:\n    value: int", []),
        ("def total_value() -> int:\n    return 1", ["COP006"]),
        ("def get_user_data() -> str:\n    return 'value'", []),
        ("async def get_user_data() -> str:\n    return 'value'", ["COP007"]),
        ("def test_example() -> None:\n    return None", []),
        ("def main() -> None:\n    return None", []),
        ("import pytest\n\n@pytest.fixture\ndef data():\n    return 1", []),
        (
            "def fetch_value() -> int:\n    result_value = 1\n    another_value = result_value\n    return another_value",
            ["COP008"],
        ),
        ("def fetch_item(values: list[int]) -> int:\n    return values[0]", []),
        ("def fetch_item(values: list[int]) -> int | None:\n    if len(values) > 0:\n        return values[0]\n    return None", []),
        ("def fill_values(values: list[int]) -> None:\n    values[0] = 1", ["COP006"]),
        ("VALUE = 10", []),
        ("class FinalClass:\n    value: int\n    def __init__(self, value: int) -> None:\n        self.value = value", ["COP010"]),
        (
            "import dataclasses\n\n"
            "@dataclasses.dataclass\n"
            "class Example:\n"
            "    value: int\n"
            "    name: str\n",
            ["COP005", "COP012", "COP005"],
        ),
        (
            "import dataclasses\n\n"
            "@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)\n"
            "class Example:\n"
            "    value: int\n",
            ["COP005"],
        ),
        (
            "import dataclasses\n\n"
            "@dataclasses.dataclass(init=False)\n"
            "class Example:\n"
            "    value: int\n",
            ["COP005", "COP012"],
        ),
        (
            "import dataclasses\n\n"
            "@dataclasses.dataclass\n"
            "class ExampleError(ValueError):\n"
            "    value: int\n",
            [],
        ),
        (
            "import dataclasses\n\n"
            "@dataclasses.dataclass\n"
            "class ExampleChild(Example):\n"
            "    value: int\n",
            [],
        ),
        ("values = {'key': 'value'}", ["COP011"]),
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
        ("import types\nvalues = types.MappingProxyType({'key': 'value'})", []),
        ("value = 1", []),
    ],
)
def test_plugin_reports(source: str, expected: list[str]) -> None:
    tree = ast.parse(source)
    messages = [item[2] for item in CommunityOfPythonFlake8Plugin(tree).run()]
    codes = [message.split(" ")[0] for message in messages]
    assert sorted(codes) == sorted(expected)
