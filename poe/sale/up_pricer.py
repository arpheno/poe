from fractions import Fraction
from typing import Union


class Pricer:
    def __init__(self, type_mapping, base):
        self.base = base
        self.type_mapping = type_mapping

    def up_price(self, item) -> Union[Fraction, float]:
        base = self.type_mapping.get(item.type, self.base)
        if item.stack_size > 50:
            base *= 1.1

        final_price_chaos: float = max(base * item.stack_size * item.initial_price, item.config_value)
        return final_price_chaos
