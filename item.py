from dataclasses import dataclass, field
from fractions import Fraction
from typing import List


def kwargs_dataclass(cls):
    Kls = dataclass(cls)

    class Als(Kls):
        def __init__(self, **kwargs):
            super().__init__(**{name: value for name, value in kwargs.items() if name in self.__annotations__})

    return Als


@kwargs_dataclass
class Item:
    inventoryId: int
    typeLine: str
    x: int
    y: int
    league: str
    stashtab:str
    stackSize: int = 1
    price: int = None
    type: str = None
    name: str=''
    sockets: tuple=()
    properties: dict=field(default_factory=dict)
    @property
    def _fractional_price(self):
        return Fraction(self.price).limit_denominator(self.stackSize)
    @property
    def fractional_price(self):
        return f"{self._fractional_price}"
    @property
    def offered_discount_volume(self):
        return (1-(self._fractional_price/self.price))*self.stackSize

    @property
    def shoplink(self):
        return f'[linkItem location="{self.inventoryId}" league="{self.league}" x="{self.x}" y="{self.y}"] ~b/o {self.fractional_price} chaos'
    @property
    def shoplink_template(self):
        return f'[linkItem location="{self.inventoryId}" league="{self.league}" x="{self.x}" y="{self.y}"] ~b/o '+'{final_price} {fx_id}'

    @property
    def type_line(self):
        return self.typeLine

    @property
    def value(self):
        return self.stackSize * self.price if self.price else 0
    @property
    def stack_size(self):
        return self.stackSize
    @property
    def map_tier(self):
        try:
            [map_properties]=[prop for prop in self.properties if prop['name']=='Map Tier']
            map_tier = int(map_properties['values'][0][0])
            return map_tier
        except:
            return None