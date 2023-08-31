from typing import List

from pydantic import BaseModel


class Property(BaseModel):
    name: str
    values: list
    displayMode: int
    type: int = None


class Item(BaseModel):
    verified: bool
    w: int
    h: int
    icon: str
    league: str
    id: str
    name: str
    typeLine: str
    baseType: str
    identified: bool
    ilvl: int
    properties: List[Property]
    descrText: str
    frameType: int
    x: int
    y: int
    inventoryId: str
    stashtab: str
    corrupted: bool = None
    explicitMods: List[str] = []
    enchantMods: List[str] = []

    def extract_property(self, identifier) -> Property:
        [prop] = [prop for prop in self.properties if prop.name == identifier]
        return prop

    @property
    def hash_key(self):
        return [{'name': self.name}, {'name': self.typeLine}]
