import typing


def process_value() -> None:
    valid_name: typing.Final = 1
    other_name: typing.Final = 2
    _: typing.Final = valid_name + other_name
