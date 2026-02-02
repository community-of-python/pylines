import typing

class SomeConstDict(typing.TypedDict):
    some_key: int
    another_key: str

const_data: typing.Final[SomeConstDict] = {"some_key": 1, "another_key": "value"}
