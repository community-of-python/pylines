import dataclasses


@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)
class SomeClient:
    value: int
