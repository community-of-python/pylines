class Engine:
    def start(self) -> None:
        pass


class Car:
    engine: Engine

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
