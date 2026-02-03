from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .violation_codes import ViolationCode


@dataclass(frozen=True)
class Violation:
    line: int
    col: int
    code: ViolationCode
