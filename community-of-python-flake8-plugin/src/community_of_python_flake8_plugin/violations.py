from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Violation:
    line: int
    col: int
    message: str
