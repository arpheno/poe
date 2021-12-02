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
    x: int
    y: int
    league: str
    stashtab:str
    type: str
    stackSize: int = 1
    price: int = None
    typeLine:str=''
    name: str=''
    sockets: tuple=()
    baseType: str=''
    properties: dict=field(default_factory=dict)
    influences: dict=field(default_factory=dict)
    corrupted:bool= False
    ilvl:int = 0
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
    def extract_property(self,identifier)->dict:
        [prop]=[prop for prop in self.properties if prop['name']==identifier]
        return prop
class Map(Item):
    @property
    def map_tier(self):
        map_tier = self.extract_property('Map Tier')['values'][0][0]
        return int(map_tier)
class SkillGem(Item):
    @property
    def level(self):
        level = self.extract_property('Level')['values'][0][0].strip('%+()Max')
        return int(level)
    @property
    def quality(self):
        try:
            level = self.extract_property('Quality')['values'][0][0].strip('%+()Max')
            return int(level)
        except:
            return 0
class Base(Item):
    @property
    def influence(self):
        influence = sorted(key for key,value in self.influences.items() if value)
        return influence
