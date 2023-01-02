import inspect
import statistics

import pandas as pd

ALT_QUALITY = {"Phantasmal", "Anomalous", "Divergent"}

div_card_rules = {}


def terrible_secret_of_space(prices):
    stack_size = 8
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    relevant_gems = [
        gem
        for gem in gems
        if "Golem" in gem["name"]
        if gem["gemLevel"] == 21
        if gem.get("gemQuality") == 23
        if gem["sparkline"]["data"]
    ]

    values = [gem["chaosValue"] for gem in relevant_gems]
    value = sum(values) / 18 / stack_size
    return value


def the_rite_of_elements(prices):
    stack_size = 5
    relevant_gems = (
        item
        for price in prices.values()
        for item in price
        if "Golem" in item["name"]
        if item["type"] == "SkillGem"
        if item["gemLevel"] == 21
        if not any(qual in item["name"] for qual in ALT_QUALITY)
        if item.get("gemQuality") == None
        if item["sparkline"]["data"]
    )
    values = pd.Series({gem["name"]: gem["chaosValue"] for gem in relevant_gems})
    return values[values < values.quantile(0.75)].mean() / stack_size


def the_cheater(prices):
    stack_size = 3
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    relevant_gems = [
        gem
        for gem in gems
        if "Awakened" in gem["name"]
        if gem["gemLevel"] == 6
        if gem.get("gemQuality") == 20
        if gem["sparkline"]["data"]
    ]

    values = pd.Series({gem["name"]: gem["chaosValue"] for gem in relevant_gems})
    return values[values < values.quantile(0.75)].mean() / stack_size


def desecrated_virtue(prices):
    stack_size = 9
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    relevant_gems = [
        gem
        for gem in gems
        if "Awakened" in gem["name"]
        if gem["gemLevel"] == 6
        if gem.get("gemQuality") == 23
        if gem["sparkline"]["data"]
    ]

    values = pd.Series({gem["name"]: gem["chaosValue"] for gem in relevant_gems})
    return values[values < values.quantile(0.75)].mean() / stack_size


def the_enlightened(prices):
    stack_size = 6
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    [relevant_gem] = [
        gem
        for gem in gems
        if "Enlighten Support" == gem["name"]
        if gem["variant"] == "3"
    ]
    value = relevant_gem["chaosValue"] / stack_size
    return value

def gemcutters_mercy(prices):
    stack_size = 3
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    relevant_gems = [
        gem
        for gem in gems
        if gem["name"] in( "Enlighten Support","Empower Support","Enhance Support")
        if gem["variant"] == "1"
    ]
    value = sum(relevant_gem["chaosValue"] for relevant_gem in relevant_gems)/3 / stack_size
    return value

def wealth_and_power(prices):
    stack_size = 11
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    [relevant_gem] = [
        gem
        for gem in gems
        if "Enlighten Support" == gem["name"]
        if gem["gemLevel"] == 4
    ]
    value = relevant_gem["chaosValue"] / stack_size
    return value


def the_dragons_heart(prices):
    stack_size = 11
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    [relevant_gem] = [
        gem for gem in gems if "Empower Support" == gem["name"] if gem["gemLevel"] == 4
    ]
    value = relevant_gem["chaosValue"] / stack_size
    return value


def the_artist(prices):
    stack_size = 11
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    [relevant_gem] = [
        gem for gem in gems if "Enhance Support" == gem["name"] if gem["gemLevel"] == 4
    ]
    value = relevant_gem["chaosValue"] / stack_size
    return value


def the_bitter_blossom(prices):
    outcomes = [
        "Added Chaos Damage Support",
        "Vicious Projectiles Support",
        "Summon Chaos Golem",
        "Chance to Poison Support",
        "Decay Support",
        "Withering Touch Support",
        "Impending Doom Support",
        "Void Manipulation Support",
        "Hexblast",
        "Caustic Arrow",
        "Bane",
        "Plague Bearer",
        "Withering Step",
        "Viper Strike",
        "Pestilent Strike",
        "Dark Pact",
        "Herald of Agony",
        "Venom Gyre",
        "Void Sphere",
        "Toxic Rain",
        "Spirit Offering",
        "Voltaxic Burst",
        "Blight",
        "Despair",
        "Desecrate",
        "Essence Drain",
        "Poisonous Concoction",
        "Forbidden Rite",
        "Cobra Lash",
        "Soulrend",
        "Contagion",
        "Wither",
        "Scourge Arrow",
    ]

    stack_size = 3
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    relevant_gems = [
        gem
        for gem in gems
        if gem["name"] in outcomes
        if gem["gemLevel"] == 21
        if gem.get("gemQuality") == 23
        if gem["sparkline"]["data"]
    ]
    values = pd.Series({gem["name"]: gem["chaosValue"] for gem in relevant_gems})
    return values[values < values.quantile(0.75)].sum() / len(outcomes) / stack_size


def the_wilted_rose(prices):
    outcomes = [
        "Discipline",
        "Smite",
        "Vitality",
        "Pyroclast Mine",
        "Rejuvenation Totem",
        "Purity of Fire",
        "Purity of Lightning",
        "Anger",
        "Purity of Elements",
        "Haste",
        "Determination",
        "Hatred",
        "Precision",
        "Purity of Ice",
        "Wrath",
        "Malevolence",
        "Stormblast Mine",
        "War Banner",
        "Pride",
        "Dread Banner",
        "Icicle Mine",
        "Grace",
        "Clarity",
        "Zealotry",
        "Defiance Banner",
        "Flesh and Stone",
        "Summon Skitterbots",
    ]
    stack_size = 7
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    relevant_gems = [
        gem
        for gem in gems
        if gem["name"] in outcomes
        if gem["gemLevel"] == 21
        if gem.get("gemQuality") == None
        if gem["sparkline"]["data"]
    ]
    values = pd.Series({gem["name"]: gem["chaosValue"] for gem in relevant_gems})
    return values[values < values.quantile(0.75)].sum()/len(outcomes) / stack_size


def deathly_designs(prices):
    outcomes = [
        "Siphoning Trap",
        "Trap and Mine Damage Support",
        "Blade Trap",
        "Multiple Traps Support",
        "Swift Assembly Support",
        "Explosive Trap",
        "Conversion Trap",
        "Bear Trap",
        "Flamethrower Trap",
        "Charged Traps Support",
        "Advanced Traps Support",
        "Fire Trap",
        "Ice Trap",
        "Lightning Trap",
        "Lightning Spire Trap",
        "Cluster Traps Support",
        "Seismic Trap",
        "Trap Support",
        "Summon Skitterbots",
    ]
    stack_size = 7
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    relevant_gems = [
        gem
        for gem in gems
        if gem["name"] in outcomes
        if gem["gemLevel"] == 21
        if gem.get("gemQuality") == None
        if gem["sparkline"]["data"]
    ]
    values = pd.Series({gem["name"]: gem["chaosValue"] for gem in relevant_gems})
    return values[values < values.quantile(0.75)].sum()/len(outcomes)/ stack_size


def dying_anguish(prices):
    stack_size = 8
    relevant_gems = (
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
        if not any(qual in item["name"] for qual in ALT_QUALITY)
        if item["variant"] == "20/20"
        if item["sparkline"]["data"]
    )
    values = pd.Series({gem["name"]: gem["chaosValue"] for gem in relevant_gems})
    return values[values < values.quantile(0.75)].mean() / stack_size


def the_puzzle(prices):
    stack_size = 5
    outcomes = [
        "Splinter of Uul-Netol",
        "Splinter of Esh",
        "Splinter of Tul",
        "Splinter of Chayula",
        "Splinter of Xoph",
    ]
    splinters = [
        item for price in prices.values() for item in price if item["name"] in outcomes
    ]
    values = [splinter["chaosValue"] for splinter in splinters]
    value = statistics.mean(values) / stack_size
    return value * 5


def the_eldritch_decay(prices):
    outcomes = [
        "Fragment of Eradication",
        "Fragment of Purification",
        "Fragment of Enslavement",
        "Fragment of Constriction",
    ]
    stack_size = 4
    relevant = [
        item for price in prices.values() for item in price if item["name"] in outcomes
    ]
    values = [item["chaosValue"] for item in relevant]
    value = sum(values)/ len(outcomes) / stack_size
    return value


def emperors_luck(prices):
    stack_size = 5
    outcomes = {
        "Blacksmith's Whetstone": 0.10830000000000001,
        "Cartographer's Chisel": 0.027000000000000003,
        "Chromatic Orb": 0.058499999999999996,
        "Jeweller's Orb": 0.0533,
        "Orb of Alchemy": 0.0323,
        "Orb of Alteration": 0.048499999999999995,
        "Orb of Augmentation": 0.10279999999999999,
        "Orb of Chance": 0.0513,
        "Orb of Fusing": 0.0333,
        "Orb of Scouring": 0.013300000000000001,
        "Orb of Transmutation": 0.2048,
    }
    value = (
                    sum(
                        prices[key][0]["chaosValue"] if key in prices else 0
                        for key, value in outcomes.items()
                    )
                    + 0.016
            ) / len(
        outcomes
    )  # Chaos orb is 1.6%
    return value / stack_size * 5


def the_bones(prices):
    stack_size = 6
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    relevant_gems = [
        gem
        for gem in gems
        if "Vaal Summon Skeletons" in gem["name"]
        if gem["gemLevel"] == 21
        if gem.get("gemQuality") == None
        if gem["sparkline"]["data"]
    ]
    values = [gem["chaosValue"] for gem in relevant_gems]
    value = statistics.mean(values) / stack_size
    return value


# def diallas_subjugation(prices):
#     stack_size = xxxcalc_stack_size(prices)
#     gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
#     relevant_gems = [
#         gem
#         for gem in gems
#         if "Support" in gem["name"]
#         if not "wakened" in gem["name"]
#         if gem["gemLevel"] == 1
#         if gem.get("gemQuality") == 23
#     ]
#     values = [gem["chaosValue"] for gem in relevant_gems]
#     value = statistics.mean(values) / stack_size
#     print(statistics.stdev(values) / stack_size)
#     return value
#


def the_cacophony(prices):
    stack_size = 8
    relevant_essences = [
        item
        for price in prices.values()
        for item in price
        if "Deafening Essence" in item["name"]
    ]
    values = [essence["chaosValue"] for essence in relevant_essences]
    value = statistics.mean(values) / stack_size
    return value * 3


def harmony_of_souls(prices):
    stack_size = 9
    relevant_essences = [
        item
        for price in prices.values()
        for item in price
        if "Shrieking Essence" in item["name"]
    ]
    values = [essence["chaosValue"] for essence in relevant_essences]
    value = statistics.mean(values) / stack_size
    return value * 9


def the_tinkerers_table(prices):
    stack_size = 5
    datapoints = 360
    outcomes = {
        "Aberrant Fossil": 35,
        "Aetheric Fossil": 20,
        "Corroded Fossil": 10,
        "Dense Fossil": 45,
        "Enchanted Fossil": 10,
        "Encrusted Fossil": 5,
        "Frigid Fossil": 15,
        "Jagged Fossil": 30,
        "Lucent Fossil": 15,
        "Metallic Fossil": 15,
        "Perfect Fossil": 10,
        "Prismatic Fossil": 10,
        "Pristine Fossil": 35,
        "Scorched Fossil": 25,
        "Shuddering Fossil": 10,
        "Tangled Fossil": 5,
    }
    outcomes = {key: value / datapoints for key, value in outcomes.items()}
    value = sum(
        prices[key][0]["chaosValue"] if key in prices else 0
        for key, value in outcomes.items()
    )
    return value / stack_size


def sambodhis_vow(prices):
    stack_size = 3
    relevant = [
        item for price in prices.values() for item in price if "Mortal " in item["name"]
    ]
    values = [item["chaosValue"] for item in relevant]
    value = statistics.mean(values) / stack_size
    return value


def the_primordial(prices):
    stack_size = 5
    relevant = [
        item
        for price in prices.values()
        for item in price
        if item["name"].startswith("Primordial ")
    ]
    values = [item["chaosValue"] for item in relevant]
    value = statistics.mean(values) / stack_size
    return value


def the_rabbits_foot(prices):
    stack_size = 8
    relevant = [
        item for price in prices.values() for item in price if item["type"] == "Vial"
    ]
    values = pd.Series({gem["name"]: gem["chaosValue"] for gem in relevant})
    return values[values < values.quantile(0.75)].mean() / stack_size * 10


def dementophobia(prices):
    stack_size = 11
    relevant = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "DeliriumOrb"
    ]
    values = [item["chaosValue"] for item in relevant]
    value = statistics.mean(values) / stack_size
    return value * 10


def disdain(prices):
    stack_size = 5
    relevant = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "DeliriumOrb"
    ]
    values = [item["chaosValue"] for item in relevant]
    value = statistics.mean(values) / stack_size
    return value


def more_is_never_enough(prices):
    stack_size = 7
    relevant = [
        item
        for price in prices.values()
        for item in price
        if item["name"].startswith("Gilded ")
        if item["name"].endswith("Scarab")
    ]
    values = [item["chaosValue"] for item in relevant]
    value = statistics.mean(values) / stack_size
    return value


def the_obscured(prices):
    stack_size = 7
    relevant = [
        item
        for price in prices.values()
        for item in price
        if item["name"].endswith("Breachstone")
        if not any(q in item["name"] for q in {"nriched", "harged", "ure", "lawless"})
    ]
    values = [item["chaosValue"] for item in relevant]
    value = statistics.mean(values) / stack_size
    return value / 5


def the_eye_of_terror(prices):
    stack_size = 8
    relevant = [
        item
        for key, price in prices.items()
        for item in price
        if key == "Chayula's Pure Breachstone"
    ]
    values = [item["chaosValue"] for item in relevant]
    value = statistics.mean(values) / stack_size
    return value


def the_long_con(prices):
    stack_size = 4
    relevant = [
        item
        for price in prices.values()
        for item in price
        if item["name"].endswith("'s Exalted Orb")
    ]
    values = [item["chaosValue"] for item in relevant]
    value = statistics.mean(values) / stack_size
    return value


def bijoux(prices):
    stack_size = 3
    relevant = [
        item
        for price in prices.values()
        for item in price
        if "Cluster Jewel" in item.get("baseType", "")
        if item.get("levelRequired") == 84
    ]
    values = [item["chaosValue"] for item in relevant]
    value = statistics.mean(values) / stack_size
    return value


div_card_rules["Bijoux"] = bijoux
div_card_rules["The Obscured"] = the_obscured
div_card_rules["The Long Con"] = the_long_con
div_card_rules["The Eye of Terror"] = the_eye_of_terror
div_card_rules["The Cheater"] = the_cheater
div_card_rules["Desecrated Virtue"] = desecrated_virtue
div_card_rules["The Enlightened"] = the_enlightened
div_card_rules["Wealth and Power"] = wealth_and_power
div_card_rules["The Dragon's Heart"] = the_dragons_heart
div_card_rules["The Bitter Blossom"] = the_bitter_blossom
div_card_rules["The Wilted Rose"] = the_wilted_rose
div_card_rules["The Artist"] = the_artist
div_card_rules["Deathly Designs"] = deathly_designs
div_card_rules["The Puzzle"] = the_puzzle
div_card_rules["The Eldritch Decay"] = the_eldritch_decay
div_card_rules["Dying Anguish"] = dying_anguish
div_card_rules["The Primordial"] = the_primordial
div_card_rules["Sambodhi's Vow"] = sambodhis_vow
div_card_rules["The Tinkerer's Table"] = the_tinkerers_table
div_card_rules["The Cacophony"] = the_cacophony
div_card_rules["Harmony of Souls"] = harmony_of_souls
div_card_rules["The Rabbit's Foot"] = the_rabbits_foot
div_card_rules["Dementophobia"] = dementophobia
div_card_rules["Disdain"] = disdain
div_card_rules["More is Never Enough"] = more_is_never_enough
div_card_rules["Emperor's Luck"] = emperors_luck
div_card_rules["The Bones"] = the_bones
div_card_rules["The Rite of Elements"] = the_rite_of_elements
div_card_rules["Terrible Secret of Space"] = terrible_secret_of_space
div_card_rules["Gemcutter's Mercy"] = gemcutters_mercy


def xxxmap_div_card_name(name: str):
    return name.lower().replace("'", "").replace(" ", "_")


def calc_stack_size(prices):
    div_card_name = inspect.stack()[1][3]
    stack_size = {xxxmap_div_card_name(name): value for name, value in prices.items()}[
        div_card_name
    ][0]["stackSize"]
    return stack_size
