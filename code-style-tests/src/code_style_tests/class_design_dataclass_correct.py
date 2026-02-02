import dataclasses


@dataclasses.dataclass(kw_only=True, slots=True, frozen=True)
class Client:
    value: int
