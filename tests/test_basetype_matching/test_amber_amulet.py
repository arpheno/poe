from poe.item import Base
from poe.matchers.base_matcher import match_base

l = [
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Warlord/Hunter",
        "levelRequired": 83,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Crusader/Redeemer",
        "levelRequired": 84,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Redeemer/Hunter",
        "levelRequired": 86,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Elder/Crusader",
        "levelRequired": 86,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Warlord/Hunter",
        "levelRequired": 85,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Crusader/Redeemer",
        "levelRequired": 86,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Warlord/Hunter",
        "levelRequired": 84,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Shaper/Redeemer",
        "levelRequired": 83,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Shaper/Warlord",
        "levelRequired": 85,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Warlord/Hunter",
        "levelRequired": 86,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Redeemer/Hunter",
        "levelRequired": 83,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Shaper/Hunter",
        "levelRequired": 85,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Shaper/Warlord",
        "levelRequired": 83,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Elder/Hunter",
        "levelRequired": 85,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Crusader/Hunter",
        "levelRequired": 86,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Elder/Hunter",
        "levelRequired": 83,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Shaper/Hunter",
        "levelRequired": 86,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Redeemer/Warlord",
        "levelRequired": 86,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Shaper/Warlord",
        "levelRequired": 86,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Crusader/Warlord",
        "levelRequired": 86,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Hunter",
        "levelRequired": 86,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Hunter",
        "levelRequired": 85,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Hunter",
        "levelRequired": 82,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Hunter",
        "levelRequired": 83,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Hunter",
        "levelRequired": 84,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Redeemer",
        "levelRequired": 86,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Crusader",
        "levelRequired": 86,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Warlord",
        "levelRequired": 86,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Elder",
        "levelRequired": 86,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Shaper",
        "levelRequired": 85,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Shaper",
        "levelRequired": 82,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Redeemer",
        "levelRequired": 85,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Warlord",
        "levelRequired": 83,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Shaper",
        "levelRequired": 86,
    },
    {"name": "Amber Amulet", "baseType": "Amber Amulet", "levelRequired": 85},
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Shaper",
        "levelRequired": 83,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Elder",
        "levelRequired": 84,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Shaper",
        "levelRequired": 84,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Elder",
        "levelRequired": 85,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Elder",
        "levelRequired": 83,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Elder",
        "levelRequired": 82,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Warlord",
        "levelRequired": 82,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Redeemer",
        "levelRequired": 83,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Warlord",
        "levelRequired": 84,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Crusader",
        "levelRequired": 82,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Crusader",
        "levelRequired": 83,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Redeemer",
        "levelRequired": 82,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Warlord",
        "levelRequired": 85,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Crusader",
        "levelRequired": 85,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Crusader",
        "levelRequired": 84,
    },
    {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Redeemer",
        "levelRequired": 84,
    },
    {"name": "Amber Amulet", "baseType": "Amber Amulet", "levelRequired": 83},
    {"name": "Amber Amulet", "baseType": "Amber Amulet", "levelRequired": 82},
    {"name": "Amber Amulet", "baseType": "Amber Amulet", "levelRequired": 86},
    {"name": "Amber Amulet", "baseType": "Amber Amulet", "levelRequired": 84},
]


def test_match_amber_amulet():
    b = Base(
        baseType="Amber Amulet",
        ilvl=83,
        x=0,
        y=0,
        league="Ultimatum",
        influences={"crusader": True},
        inventoryId=0,
        stashtab="",
    )
    assert match_base(l, b) == {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "variant": "Crusader",
        "levelRequired": 83,
    }


def test_match_amber_amulet():
    b = Base(
        baseType="Amber Amulet",
        ilvl=83,
        x=0,
        y=0,
        league="Ultimatum",
        inventoryId=0,
        stashtab="",
    )
    assert match_base(l, b) == {
        "name": "Amber Amulet",
        "baseType": "Amber Amulet",
        "levelRequired": 83,
    }
