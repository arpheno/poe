from poe.item.newitems.blueprint import Blueprint
from poe.item.newitems.logbook import ExpeditionLogbook
from poe.valuation.framework.price_store import HashKeyPriceStore
from poe.valuation.framework.tft_adapter.adapter import TftAdapter


def test_match_logbooks():
    tft_adapter = TftAdapter()
    tft_valuations = tft_adapter.adapt()
    price_store = HashKeyPriceStore(tft_valuations)
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
    logbook=ExpeditionLogbook(**raw)
    price_store.query(logbook.hash_key)
    pass
def test_match_blueprint():
    raw = {'verified': False, 'w': 1, 'h': 1,
           'icon': 'https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvSGVpc3QvQmx1ZXByaW50Tm90QXBwcm92ZWQ4IiwidyI6MSwiaCI6MSwic2NhbGUiOjF9XQ/cc90ce9113/BlueprintNotApproved8.png',
           'league': 'Sanctum', 'id': '125db449cc3da67445a5997557dee07ec08d51576017a3d4e949cf955caff4f6', 'name': '',
           'typeLine': 'Dutiful Blueprint: Records Office of Apprehension', 'baseType': 'Blueprint: Records Office',
           'identified': True, 'ilvl': 83, 'properties': [
            {'name': 'Heist Target: {0}', 'values': [['Enchanted Armaments', 0]], 'displayMode': 3, 'type': 47},
            {'name': 'Area Level', 'values': [['83', 0]], 'displayMode': 0, 'type': 34},
            {'name': 'Wings Revealed', 'values': [['1/3', 0]], 'displayMode': 0, 'type': 35},
            {'name': 'Escape Routes Revealed', 'values': [['1/6', 0]], 'displayMode': 0, 'type': 36},
            {'name': 'Reward Rooms Revealed', 'values': [['3/21', 0]], 'displayMode': 0, 'type': 37},
            {'name': 'Requires {1} (Level {0})', 'values': [['2', 0], ['Lockpicking', 0]], 'displayMode': 3,
             'type': 38},
            {'name': 'Requires {1} (Level {0})', 'values': [['5', 0], ['Counter-Thaumaturgy', 0]], 'displayMode': 3,
             'type': 42},
            {'name': 'Requires {1} (Level {0})', 'values': [['2', 0], ['Deception', 0]], 'displayMode': 3, 'type': 45},
            {'name': 'Item Quantity', 'values': [['+32%', 1]], 'displayMode': 0, 'type': 2},
            {'name': 'Item Rarity', 'values': [['+18%', 1]], 'displayMode': 0, 'type': 3},
            {'name': 'Alert Level Reduction', 'values': [['+12%', 1]], 'displayMode': 0},
            {'name': 'Time Before Lockdown', 'values': [['+12%', 1]], 'displayMode': 0},
            {'name': 'Maximum Alive Reinforcements', 'values': [['+12%', 1]], 'displayMode': 0, 'type': 4}],
           'explicitMods': ['Patrol Packs take 27% reduced damage', 'Players have 8% less Evasion per 25% Alert Level'],
           'descrText': 'Use Intelligence to Reveal additional Wings and Rooms by talking to certain NPCs in the Rogue Harbour. Give this Blueprint to Adiyah to embark on the Grand Heist.',
           'frameType': 1, 'x': 9, 'y': 4, 'inventoryId': 'Stash8', 'stashtab': 'noindex'}
    tft_adapter = TftAdapter()
    tft_valuations = tft_adapter.adapt()
    price_store = HashKeyPriceStore(tft_valuations)
    result=price_store.query(Blueprint(**raw).hash_key)
    assert result