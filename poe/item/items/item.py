from dataclasses import field
from fractions import Fraction

from poe.item import kwargs_dataclass


@kwargs_dataclass
class Item:
    inventoryId: str
    x: int
    y: int
    league: str
    stashtab: str
    type: str
    stackSize: int = 1
    price: int = None
    typeLine: str = ""
    sockets: tuple = field(default_factory=tuple)
    baseType: str = ""
    properties: dict = field(default_factory=lambda: [{}])
    influences: dict = field(default_factory=dict)
    corrupted: bool = False
    ilvl: int = 0
    enchantMods: list = field(default_factory=list)

    @property
    def _fractional_price(self):
        return Fraction(self.price).limit_denominator(self.stackSize)

    @property
    def fractional_price(self):
        return f"{self._fractional_price}"

    @property
    def offered_discount_volume(self):
        return (1 - (self._fractional_price / self.price)) * self.stackSize

    @property
    def shoplink(self):
        return f'[linkItem location="{self.inventoryId}" league="{self.league}" x="{self.x}" y="{self.y}"] ~b/o {self.fractional_price} chaos'

    @property
    def shoplink_template(self):
        return (
            f'[linkItem location="{self.inventoryId}" league="{self.league}" x="{self.x}" y="{self.y}"] ~b/o '
            + "{final_price} {currency}"
        )

    @property
    def name(self):
        return self.typeLine

    @property
    def config_value(self):
        return self.stackSize * self.price if self.price else 0
    @property
    def simple_value(self):
        return self.price

    @property
    def stack_size(self):
        return self.stackSize

    def extract_property(self, identifier) -> dict:
        [prop] = [prop for prop in self.properties if prop["name"] == identifier]
        return prop

    def match(self, prices):
        candidates = prices.get(self.name) or prices.get(self.typeLine) or prices.get(self.baseType)
        return candidates[0]

    def determine_price(self, prices: dict,values:dict):
        match = self.match(prices)
        if not match:
            self.price=None
            return
        self.price = match and match["chaosValue"]
        # if not match.get("receiveSparkLine"):
        #     print(f"High uncertainty on {self.name}, adjusting x2")
        #     self.price *= 2
        if (total_change :=match.get("receiveSparkLine",{'totalChange':0})['totalChange']) < -60:
            incr = (-100 /total_change)*0.5
            print(f'Adjusting {match["name"]} by {1/incr}')
            self.price *= incr
        self.price=max(self.price,values.get(self.typeLine,0))
