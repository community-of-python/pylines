class Example:
    value: str

    def __init__(self, value: str) -> None:
        self.value = value


def fetch_value(example: Example) -> str:
    return example.value
