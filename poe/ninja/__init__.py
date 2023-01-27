import time
from collections import ChainMap

from poe.ninja.askers.facade import asker
from constants import LEAGUE

NINJA_ITEM_TYPES = (
    "Fragment",
    "Currency",
    "Scarab",
    "Oil",
    "Fossil",
    "Resonator",
    # "Prophecy",
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
    "Vial",
    "ClusterJewel",
    "Beast",
)
CHAOS_ORB = {"Chaos Orb": [{"name": "Chaos Orb", "type": "Currency", "chaosValue": 1}]}


def retrieve_prices(currencies=NINJA_ITEM_TYPES,league=LEAGUE):
    print(f"Retrieving prices from ninja", end="")
    start = time.time()
    result = ChainMap(
        CHAOS_ORB,
        *[asker(curr,league=league) for curr in currencies],
    )
    print(f"Done in {time.time() - start:.2f} seconds")
    return result
