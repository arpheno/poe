from poe.item.newitems.logbook import ExpeditionLogbook


def test_parse_logbook():
    raw = {'verified': False, 'w': 1, 'h': 1,
           'icon': 'https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvTWFwcy9FeHBlZGl0aW9uQ2hyb25pY2xlMyIsInciOjEsImgiOjEsInNjYWxlIjoxfV0/2802fe605e/ExpeditionChronicle3.png',
           'league': 'Sanctum', 'id': 'a70d79b2974af86a4ea96963f108259f23913950ff251c63f20a6204adcad240', 'name': '',
           'typeLine': 'Expedition Logbook', 'baseType': 'Expedition Logbook', 'identified': True, 'ilvl': 83,
           'properties': [{'name': 'Area Level', 'values': [['83', 0]], 'displayMode': 0, 'type': 34}], 'logbookMods': [
            {'name': 'Dried Riverbed', 'faction': {'id': 'Faction1', 'name': 'Druids of the Broken Circle'},
             'mods': ['Remnants have 26% chance to have an additional Suffix Modifier',
                      'Area contains an additional Underground Area']},
            {'name': 'Shipwreck Reef', 'faction': {'id': 'Faction2', 'name': 'Black Scythe Mercenaries'},
             'mods': ['29% increased quantity of Artifacts dropped by Monsters',
                      'Area contains 28% increased number of Runic Monster Markers']},
            {'name': 'Rotting Temple', 'faction': {'id': 'Faction2', 'name': 'Black Scythe Mercenaries'},
             'mods': ['12% increased Explosive Radius', '18% increased number of Explosives']}],
           'descrText': 'Take this item to Dannig in your Hideout to open portals to an expedition.', 'frameType': 0,
           'x': 4, 'y': 4, 'inventoryId': 'Stash8', 'stashtab': 'noindex'}
    hash_key = ExpeditionLogbook(**raw).hash_key
    assert hash_key ==[{'area_level': 83, 'logbook_faction': 'Druids of the Broken Circle'},
                      {'area_level': 83, 'logbook_faction': 'Black Scythe Mercenaries'},
                      {'area_level': 83, 'logbook_faction': 'Black Scythe Mercenaries'}]
