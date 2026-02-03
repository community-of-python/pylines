from __future__ import annotations

import ast

import pytest

from community_of_python_flake8_plugin.plugin import CommunityOfPythonFlake8Plugin


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("from os import name", ["COP002"]),
        ("from x import a, b, c", ["COP001"]),
        ("value: str = 'hello'", ["COP003"]),
        ("def total_value() -> int:\n    return 1", ["COP006"]),
        ("def get_user_data() -> str:\n    return 'value'", ["COP007", "COP006"]),
        (
            "def fetch_value() -> int:\n    result_value = 1\n    another_value = result_value\n    return another_value",
            ["COP008"],
        ),
        ("def fetch_item(values: list[int]) -> int:\n    return values[0]", ["COP004"]),
        ("def fetch_item(values: list[int]) -> int | None:\n    if len(values) > 0:\n        return values[0]\n    return None", []),
        ("VALUE = 10", ["COP009"]),
        ("class FinalClass:\n    value: int\n    def __init__(self, value: int) -> None:\n        self.value = value", ["COP010", "COP012"]),
        ("values = {'key': 'value'}", ["COP011"]),
        ("import types\nvalues = types.MappingProxyType({'key': 'value'})", []),
    ],
)
def test_plugin_reports(source: str, expected: list[str]) -> None:
    tree = ast.parse(source)
    messages = [item[2] for item in CommunityOfPythonFlake8Plugin(tree).run()]
    codes = [message.split(" ")[0] for message in messages]
    assert codes == expected
