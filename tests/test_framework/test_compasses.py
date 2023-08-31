from poe.valuation.framework.compass_name_matcher import find_matches
from poe.valuation.framework.tft_adapter.adapter import TftAdapter

mods = ['Boss drop Unique Item',
                  'Boss drop Shaper Guardian Map',
                  'Boss drop Elder Guardian Map',
                  'Boss drop Conqueror Map',
                  '20% Pack Size Unidentified Map',
                  'Additional Monsters deal Fire',
                  'Additional Monsters deal Cold',
                  'Additional Monsters deal Lightning',
                  'Additional Monsters deal Physical',
                  'Additional Monsters deal Chaos',
                  'Unique Monsters drop Corrupted Items',
                  'Maps have 20% Quality',
                  'Quality of Maps Applies to Rarity',
                  'Areas are Alluring',
                  'Areas contain Einhar',
                  'Areas contain Alva',
                  'Areas contain Niko',
                  'Areas contain Jun',
                  '2 additional Strongbox Corrupted & Rare',
                  'Boss Corrupted Map drop Vaal Items',
                  '25% increased Magic Pack Size',
                  'Areas inhabited Rogue Exiles',
                  'Rare Maps contain Rare Monster Packs',
                  'Players cannot take Reflected Damage',
                  'Areas contain Mysterious Barrels',
                  'Areas contain Mysterious Barrels',
                  'Areas contain Mysterious Barrels',
                  'Areas contain Mysterious Barrels',
                  'Areas contain Mysterious Barrels',
                  'Strongbox Enraged & Increased Quant',
                  'Areas contain Hunted Traitors',
                  'Monsters Convert when Killed',
                  'Life & Mana Flasks Instant',
                  'Boss Accompanied by Bodyguards',
                  'Areas contain Breach',
                  'Breaches belong to Xoph',
                  'Breaches belong to Tul',
                  'Breaches belong to Esh',
                  'Breaches belong to Uul-Netol',
                  'Breaches belong to Chayula',
                  'Areas contain Abyss',
                  'Areas contain Gloom Shrine',
                  'Areas contain Resonating Shrine',
                  'Areas contain Essence',
                  'Maps Corrupted with 8 Modifiers',
                  'Create Copy of Beasts',
                  'Expedition Runic Monster Markers',
                  'Legion Splinters & Emblems Duplicate',
                  'Metamorph Catalysts Duplicate',
                  'Blight Oils Found 1 Tier Higher',
                  'Delirium Reward fill faster',
                  'Harvests contain Blue Plants',
                  'Harvests contain Purple Plants',
                  'Harvests contain Yellow Plants',
                  'Heist Contracts have Implicit',
                  'Ritual Rerolling Favours No Cost',
                  'Harbingers drop Shards',
                  'Vaal Soul on Kill',
                  'Items by Vaal Monsters chance Corrupted',
                  'Attract Monsters from Beyond',
                  'Possessed Monsters drop Rusted Scarab',
                  'Possessed Monsters drop Polished Scarab',
                  'Possessed Monsters drop Gilded Scarab',
                  'Areas contain Tormented Heretic',
                  'Areas contain Tormented Graverobber',
                  'Vaal Gifts of the Red Queen/Sacrificed',
                  "Vaal Don't Apply Soul Gain Prevention",
                  'Areas contain Legion',
                  'Areas contain Metamorph',
                  'Areas contain Blight',
                  'Mirror of Delirium',
                  'Areas contain Harvest Sacred Grove',
                  "Areas contain Heist Smuggler's Cache",
                  'Areas contain Ritual Altars']


def test_compass_parses():
    adapter=TftAdapter()
    adapter.adapt()
def test_matching_compass_names():
    cutoffs = [0.8, 0.6, 0.45, 0.4, 0.3]
    a=['asdasd','cvcvcvcvcvcvccccc']
    b=['asdasdasdasdasdasdasdasdasd','cvcvcvvsdfdsfdsfsdfdsfsdfcvcvcvccccc']
    find_matches(a,b,cutoffs)
def test_match_tft():
    adapter = TftAdapter()
    response = adapter.adapt()
    response_dict = {v.key.get('name'): v.estimate for v in response if 'compass' in v.tags if
                     not '16' in v.key.get('name', '')}
    list2 = list(response_dict.keys())
    list1 = mods
    cutoffs = [0.7, 0.6, 0.5, 0.45]

    find_matches(list1,list2,cutoffs)
