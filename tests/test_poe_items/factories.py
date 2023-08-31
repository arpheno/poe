import factory

from poe.item.newitems.logbook import Faction, LogbookMod, ExpeditionLogbook
from tests.test_poe_items.test_logbooks import fake


class FactionFactory(factory.Factory):
    class Meta:
        model = Faction

    id = factory.LazyFunction(fake.uuid4)
    name = factory.LazyFunction(fake.word)


class LogbookModFactory(factory.Factory):
    class Meta:
        model = LogbookMod

    name = factory.LazyFunction(fake.word)
    faction = factory.SubFactory(FactionFactory)
    mods = factory.List([factory.LazyFunction(fake.sentence) for _ in range(2)])


class ExpeditionLogbookFactory(factory.Factory):
    class Meta:
        model = ExpeditionLogbook

    verified = False
    w = 1
    h = 1
    icon = factory.LazyFunction(fake.url)
    league = factory.LazyFunction(fake.word)
    id = factory.LazyFunction(fake.uuid4)
    name = ""
    typeLine = "Expedition Logbook"
    baseType = "Expedition Logbook"
    identified = True
    ilvl = factory.LazyFunction(fake.random_int)
    properties = [{"name": "Area Level", "values": [[str(fake.random_int), 0]], "displayMode": 0, "type": 34}]
    logbookMods = factory.List([LogbookModFactory() for _ in range(3)])
    descrText = "Take this item to Dannig in your Hideout to open portals to an expedition."
    frameType = 0
    x = 4
    y = 4
    inventoryId = "Stash8"
    stashtab = "noindex"
