from __future__ import annotations

from typing import TypedDict


class ViolationCode(TypedDict):
    code: str
    description: str


VIOLATION_CODES: list[ViolationCode] = [
    {
        "code": "COP001",
        "description": "Use module import when importing more than two names",
    },
    {
        "code": "COP002",
        "description": "Import standard library modules as whole modules",
    },
    {
        "code": "COP003",
        "description": "Avoid explicit scalar type annotations",
    },
    {
        "code": "COP004",
        "description": "Name must be at least 8 characters",
    },
    {
        "code": "COP005",
        "description": "Function name must be a verb",
    },
    {
        "code": "COP006",
        "description": "Avoid get_ prefix in async function names",
    },
    {
        "code": "COP007",
        "description": "Avoid temporary variables used only once",
    },
    {
        "code": "COP008",
        "description": "Classes should be marked typing.final",
    },
    {
        "code": "COP009",
        "description": "Wrap module dictionaries with types.MappingProxyType",
    },
    {
        "code": "COP010",
        "description": "Use dataclasses with kw_only=True, slots=True, frozen=True",
    },
]


def get_violation_description(code: str) -> str | None:
    """Get the description for a given violation code."""
    for violation in VIOLATION_CODES:
        if violation["code"] == code:
            return violation["description"]
    return None


def get_all_violation_codes() -> list[str]:
    """Get all violation codes."""
    return [violation["code"] for violation in VIOLATION_CODES]