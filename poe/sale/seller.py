from dataclasses import dataclass
from typing import Callable

from poe.sale.layouters.base import Layouter


@dataclass
class Seller:
    up_price: Callable
    layouter: Layouter
    cleaning_rules: list[str]

    def sell(self, inventory):
        register = inventory.copy()
        register["final_price_chaos"] = register.apply(self.up_price, axis=1)
        register = register.query(f'({")&(".join(self.cleaning_rules)})')
        register = self.layouter.layout(register)
        return register
