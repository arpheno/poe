from dataclasses import dataclass
from itertools import groupby
from statistics import mean
from typing import Dict, Callable

import pandas as pd

from poe.ninja import retrieve_prices


@dataclass
class Horticrafter:
    prices: Dict

    def transform(self, filter: Callable, lifeforce: str, lifeforce_cost: int):
        items = pd.DataFrame(
            [(name, item[0]['chaosValue']) for name, item in self.prices.items() if filter(name, item)],
            columns=['name', 'cost'])
        items['value'] = items['cost'].mean() - prices[lifeforce][0]['chaosValue'] * lifeforce_cost
        items['profit'] = items['value'] - items['cost']
        items = items.query('profit > 0')
        return items

    def delirium_orbs(self):
        return self.transform(lambda name, item: "Delirium Orb" in name, 'Primal Crystallised Lifeforce', 30)

    def catalysts(self):
        return self.transform(lambda name, item: "Catalyst" in name, 'Vivid Crystallised Lifeforce', 30)

    def scarabs(self):
        return self.transform(lambda name, item: "Scarab" in name and "Gilded" in name, 'Wild Crystallised Lifeforce',
                              30)

    def essences(self):
        return self.transform(lambda name, item: "Essence" in name and "Deafening" in name, 'Primal Crystallised Lifeforce',
                              30)


if __name__ == '__main__':
    prices = retrieve_prices(['Currency', 'DeliriumOrb', 'Scarab', 'Essence'])
    horticrafter = Horticrafter(prices)
    print(horticrafter.scarabs())
    print(horticrafter.catalysts())
    print(horticrafter.delirium_orbs())
    print(horticrafter.essences())
