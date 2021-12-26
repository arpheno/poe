from collections import ChainMap

from poe.ninja.askers.facade import asker

NINJA_ITEM_TYPES = (
    "Fragment",
    "Currency",
    "Scarab",
    "Oil",
    "Fossil",
    "Resonator",
    "Prophecy",
    "Incubator",
    "UniqueMap",
    "UniqueJewel",
    "UniqueFlask",
    "UniqueArmour",
    "UniqueWeapon",
    "UniqueAccessory",
    "Essence",
    "DeliriumOrb",
    "DivinationCard",
    "Map",
    "SkillGem",
    "BaseType",
    'Vial',
)
def retrieve_prices(currencies=NINJA_ITEM_TYPES):

    return ChainMap(*[asker(curr) for curr in currencies])

