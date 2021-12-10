from dataclasses import dataclass


def kwargs_dataclass(cls):
    Kls = dataclass(cls)

    class Als(Kls):
        def __init__(self, **kwargs):
            super().__init__(**{name: value for name, value in kwargs.items() if name in self.__annotations__})

    return Als


