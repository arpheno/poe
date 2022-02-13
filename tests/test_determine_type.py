from poe.item.type_determiner import determine_type


def test_determine_influence():
    ring = {
        "influences": {"crusader": True},
        "name": "Moonstone Ring",
        "typeLine": "Moonstone Ring",
        "baseType": "Moonstone Ring",
        "identified": False,
        "ilvl": 73,
    }
    assert determine_type(ring,{}) == 'Base'