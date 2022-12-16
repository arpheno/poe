import math
from fractions import Fraction
from typing import Union

import pandas as pd

from poe.item import kwargs_dataclass
from poe.sale.fake_fraction import FakeFraction
from poe.sale.layouters.base import Layouter


@kwargs_dataclass
class DivineLayouter(Layouter):
    divine_value: Union[float, int]
    min_trade_value: int = 50

    def layout(self, register: pd.DataFrame) -> pd.DataFrame:
        register["currency"] = register.final_price_chaos.map(
            lambda x: "divine" if x > self.divine_value else "chaos"
        )
        funcs = {"chaos": self.turn_to_fraction, "divine": self.turn_to_divine}
        register["final_price"] = register.apply(
            lambda item: funcs[item.currency](item.final_price_chaos, item.stack_size),
            axis=1,
        )
        return register
    def turn_to_divine(self, final_price_chaos, stack_size):
        numerator = final_price_chaos / self.divine_value
        numerator, denominator = (
            (1, round(ratio))
            if ((ratio := stack_size / numerator) > 1)
            else (numerator, stack_size)
        )
        return FakeFraction(round(numerator, 1), denominator)

    def turn_to_fraction(self, final_price_chaos, stack_size):
        best_fraction = Fraction(final_price_chaos / stack_size).limit_denominator(
            stack_size
        )

        if best_fraction.numerator > self.min_trade_value:
            numerator, denominator = (
                best_fraction.numerator,
                best_fraction.denominator,
            )
        elif best_fraction.numerator > 0:
            numerator, denominator = (
                self.min_trade_value,
                math.ceil(
                    best_fraction.denominator
                    * (self.min_trade_value / best_fraction.numerator)
                ),
            )
        else:
            numerator, denominator = (0, 1)

        return FakeFraction(numerator, denominator)