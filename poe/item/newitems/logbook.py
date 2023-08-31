from pydantic import BaseModel, validator

from poe.item.newitems.base_item_model import Item
from poe.valuation.framework.valuation import domain_hash_key


class Faction(BaseModel):
    id: str
    name: str


class LogbookMod(BaseModel):
    name: str
    faction: Faction
    mods: list


class ExpeditionLogbook(Item):
    logbookMods: list[LogbookMod]

    @property
    def area_level(self) -> int:
        return int(self.extract_property('Area Level').values[0][0])

    @property
    def factions(self) -> list:
        factions = []
        for mod in self.logbookMods:
            factions.append(mod.faction.name)
        return factions

    @property
    def hash_key(self):
        return [{'area_level': self.area_level, 'logbook_faction': faction} for faction in self.factions]
