from poe.item.newitems.blueprint import Blueprint
from poe.item.newitems.contract import Contract

contract = {'verified': False, 'w': 1, 'h': 1,
            'icon': 'https://web.poecdn.com/gen/image/WzI1LDE0LHsiZiI6IjJESXRlbXMvQ3VycmVuY3kvSGVpc3QvQ29udHJhY3RJdGVtNSIsInciOjEsImgiOjEsInNjYWxlIjoxfV0/fd1a9eb91f/ContractItem5.png',
            'league': 'Sanctum', 'id': '2d60addabf3242effb336942ea53431d77248152ddd4fea479dd5dd2b7c45309',
            'name': 'Mind Manifesto', 'typeLine': 'Contract: Prohibited Library',
            'baseType': 'Contract: Prohibited Library', 'identified': True, 'ilvl': 85,
            'properties': [{'name': 'Client', 'values': [['Grond Ironeye', 0]], 'displayMode': 0},
                           {'name': 'Heist Target: {0} ({1})',
                            'values': [['Golden Hetzapal Idol', 0], ['High Value', 0]],
                            'displayMode': 3, 'type': 47},
                           {'name': 'Area Level', 'values': [['83', 0]], 'displayMode': 0, 'type': 34},
                           {'name': 'Requires {1} (Level {0})', 'values': [['3', 0], ['Perception', 0]],
                            'displayMode': 3,
                            'type': 40},
                           {'name': 'Item Quantity', 'values': [['+52%', 1]], 'displayMode': 0, 'type': 2},
                           {'name': 'Item Rarity', 'values': [['+31%', 1]], 'displayMode': 0, 'type': 3},
                           {'name': 'Alert Level Reduction', 'values': [['+20%', 1]], 'displayMode': 0},
                           {'name': 'Time Before Lockdown', 'values': [['+20%', 1]], 'displayMode': 0},
                           {'name': 'Maximum Alive Reinforcements', 'values': [['+20%', 1]], 'displayMode': 0,
                            'type': 4}],
            'enchantMods': ['Completing a Heist generates 3 additional Reveals',
                            'Heist Chests have 25% chance to contain nothing'],
            'explicitMods': ['Players cannot inflict Exposure', 'Guards deal 29% increased Damage',
                             'Monsters have 50% increased Accuracy Rating',
                             'Monsters have a 20% chance to cause Elemental Ailments on Hit',
                             'Players have -20% to amount of Suppressed Spell Damage Prevented'],
            'descrText': 'Give this Contract to Adiyah in the Rogue Harbour to embark on the Heist.',
            'flavourText': ['"I found the tomb in the first place, and they had the nerve to empty it without me! \r',
                            'Reckon it\'ll make a fine trophy for my efforts."'], 'frameType': 2, 'x': 10, 'y': 8,
            'inventoryId': 'Stash22', 'stashtab': '3'}


def test_parse_heist_contract():
    hash_key = Contract(**contract).hash_key
    assert hash_key == [{'area_level': 83, 'heist_type': 'Perception'}]


def test_parse_heist_blueprint():
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
    hash_key = Blueprint(**raw).hash_key
    assert hash_key == [{'area_level': 83, 'heist_type': 'Enchanted Armaments', 'wings': 3},
                        {'area_level': 83, 'heist_type': 'Enchanted Armaments', 'wings': None}]
