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

    def layout(self, data: pd.DataFrame) -> pd.DataFrame:
        data["currency"] = data.final_price_chaos.map(
            lambda x: "divine" if x > self.divine_value else "chaos"
        )
        funcs = {"chaos": self.turn_to_chaos, "divine": self.turn_to_divine}
        data["final_price"] = data.apply(
            lambda item: funcs[item.currency](item.final_price_chaos, item.stack_size),
            axis=1,
        )
        return data
    def turn_to_divine(self, final_price_chaos, stack_size):
        numerator = final_price_chaos / self.divine_value
        numerator, denominator = (
            (1, round(ratio))
            if ((ratio := stack_size / numerator) > 1)
            else (numerator, stack_size)
        )
        if denominator== 1:
            return FakeFraction(round(numerator, 1), denominator)
        else:
            return FakeFraction(int(round(numerator, 0)), denominator)

    def turn_to_chaos(self, final_price_chaos, stack_size):
        return  FakeFraction(int(final_price_chaos), stack_size)

