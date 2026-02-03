from __future__ import annotations
import typing
from enum import Enum
from typing import TypedDict


class ViolationCodeItem(TypedDict):
    code: str
    description: str


class ViolationCode(Enum):
    MODULE_IMPORT: typing.ClassVar[ViolationCodeItem] = {
        "code": "COP001",
        "description": "Use module import when importing more than two names",
    }
    STDLIB_IMPORT: typing.ClassVar[ViolationCodeItem] = {
        "code": "COP002",
        "description": "Import standard library modules as whole modules",
    }
    SCALAR_ANNOTATION: typing.ClassVar[ViolationCodeItem] = {
        "code": "COP003",
        "description": "Avoid explicit scalar type annotations",
    }
    NAME_LENGTH: typing.ClassVar[ViolationCodeItem] = {
        "code": "COP004",
        "description": "Name must be at least 8 characters",
    }
    FUNCTION_VERB: typing.ClassVar[ViolationCodeItem] = {
        "code": "COP005",
        "description": "Function identifier must be a verb",
    }
    ASYNC_GET_PREFIX: typing.ClassVar[ViolationCodeItem] = {
        "code": "COP006",
        "description": "Avoid get_ prefix in async function names",
    }
    TEMPORARY_VARIABLE: typing.ClassVar[ViolationCodeItem] = {
        "code": "COP007",
        "description": "Avoid temporary variables used only once",
    }
    FINAL_CLASS: typing.ClassVar[ViolationCodeItem] = {
        "code": "COP008",
        "description": "Classes should be marked typing.final",
    }
    MAPPING_PROXY: typing.ClassVar[ViolationCodeItem] = {
        "code": "COP009",
        "description": "Wrap module dictionaries with types.MappingProxyType",
    }
    DATACLASS_CONFIG: typing.ClassVar[ViolationCodeItem] = {
        "code": "COP010",
        "description": "Use dataclasses with kw_only=True, slots=True, frozen=True",
    }
