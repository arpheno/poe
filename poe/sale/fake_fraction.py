from dataclasses import dataclass
from typing import Union


@dataclass
class FakeFraction:
    numerator: Union[str, int, float]
    denominator: int

    def __str__(self):
        return (
            f"{self.numerator}/{self.denominator}"
            if self.denominator != 1
            else f"{self.numerator}"
        )
