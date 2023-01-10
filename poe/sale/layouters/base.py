import math
from fractions import Fraction
from typing import Union

import pandas as pd

from poe.item import kwargs_dataclass
from poe.sale.fake_fraction import FakeFraction


class Layouter:
    def layout(self, register: pd.DataFrame) -> pd.DataFrame:
        pass
    def turn_to_exalt(self, final_price_chaos, stack_size):
        pass
    def turn_to_fraction(self, final_price_chaos, stack_size):
        pass