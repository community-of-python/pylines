import dataclasses


@dataclasses.dataclass
class SomeClient:
    value: int

    def __init__(self, value: int) -> None:
        self.value = value
