from dataclasses import dataclass
from typing import Callable


@dataclass
class Seller:
    turn_to_fraction: Callable
    up_price: Callable
    cleaning_rules: list[str]

    def sell(self, inventory):
        register = inventory.copy()
        register["up_priced_value_fx"] = register.apply(self.up_price, axis=1)
        register["final_price"] = register.apply(self.turn_to_fraction, axis=1)
        register = register.query(f'({")&(".join(self.cleaning_rules)})')
        return register