import inspect
import statistics

ALT_QUALITY = ("Phantasmal", "Anomalous", "Divergent")


def terrible_secret_of_space(prices):
    stack_size = xxxcalc_stack_size(prices)
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    relevant_gems = [
        gem for gem in gems if "Golem" in gem["name"] if gem["gemLevel"] == 21 if gem.get("gemQuality") == 23
    ]

    values = [gem["chaosValue"] for gem in relevant_gems]
    value = statistics.mean(values) / stack_size
    return value


def the_rite_of_elements(prices):
    stack_size = xxxcalc_stack_size(prices)
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    relevant_gems = [
        gem
        for gem in gems
        if not any(qual in gem["name"] for qual in ALT_QUALITY)
        if "Golem" in gem["name"]
        if gem["gemLevel"] == 21
        if gem.get("gemQuality") == None
    ]

    values = [gem["chaosValue"] for gem in relevant_gems]
    value = statistics.mean(values) / stack_size
    return value


def the_cheater(prices):
    stack_size = xxxcalc_stack_size(prices)
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    relevant_gems = [
        gem for gem in gems if "Awakened" in gem["name"] if gem["gemLevel"] == 6 if gem.get("gemQuality") == 20
    ]

    values = [gem["chaosValue"] for gem in relevant_gems]
    value = statistics.mean(values) / stack_size
    return value


def desecrated_virtue(prices):
    stack_size = xxxcalc_stack_size(prices)
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    relevant_gems = [
        gem for gem in gems if "Awakened" in gem["name"] if gem["gemLevel"] == 6 if gem.get("gemQuality") == 23
    ]

    values = [gem["chaosValue"] for gem in relevant_gems]
    value = statistics.mean(values) / stack_size
    return value


def the_enlightened(prices):
    stack_size = xxxcalc_stack_size(prices)
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    relevant_gems = [
        gem for gem in gems if "Enlighten" in gem["name"] if gem["gemLevel"] == 3 if gem.get("gemQuality") == None
    ]
    values = [gem["chaosValue"] for gem in relevant_gems]
    value = statistics.mean(values) / stack_size
    return value


def wealth_and_power(prices):
    stack_size = xxxcalc_stack_size(prices)
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    relevant_gems = [gem for gem in gems if "Enlighten" in gem["name"] if gem["gemLevel"] == 4]
    values = [gem["chaosValue"] for gem in relevant_gems]
    value = statistics.mean(values) / stack_size
    return value


def the_dragons_heart(prices):
    stack_size = xxxcalc_stack_size(prices)
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    relevant_gems = [gem for gem in gems if "Empower" in gem["name"] if gem["gemLevel"] == 4]
    values = [gem["chaosValue"] for gem in relevant_gems]
    value = statistics.mean(values) / stack_size
    return value


def the_artist(prices):
    stack_size = xxxcalc_stack_size(prices)
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    relevant_gems = [gem for gem in gems if "Enhance" in gem["name"] if gem["gemLevel"] == 4]
    values = [gem["chaosValue"] for gem in relevant_gems]
    value = statistics.mean(values) / stack_size
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

    stack_size = xxxcalc_stack_size(prices)
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    relevant_gems = [
        gem for gem in gems if gem["name"] in outcomes if gem["gemLevel"] == 21 if gem.get("gemQuality") == 23
    ]
    values = [gem["chaosValue"] for gem in relevant_gems]
    value = statistics.mean(values) / stack_size
    return value


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
    stack_size = xxxcalc_stack_size(prices)
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    relevant_gems = [
        gem for gem in gems if gem["name"] in outcomes if gem["gemLevel"] == 21 if gem.get("gemQuality") == None
    ]
    values = [gem["chaosValue"] for gem in relevant_gems]
    value = statistics.mean(values) / stack_size
    print(statistics.stdev(values) / stack_size)
    return value


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
    stack_size = xxxcalc_stack_size(prices)
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    relevant_gems = [
        gem for gem in gems if gem["name"] in outcomes if gem["gemLevel"] == 21 if gem.get("gemQuality") == None
    ]
    values = [gem["chaosValue"] for gem in relevant_gems]
    value = statistics.mean(values) / stack_size
    print(statistics.stdev(values) / stack_size)
    return value


def dying_anguish(prices):

    stack_size = xxxcalc_stack_size(prices)
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    relevant_gems = [
        gem
        for gem in gems
        if any(qual in gem["name"] for qual in ALT_QUALITY)
        if gem["gemLevel"] == 20
        if gem.get("gemQuality") == 20
    ]
    values = [gem["chaosValue"] for gem in relevant_gems]
    value = statistics.mean(values) / stack_size
    print(statistics.stdev(values) / stack_size)
    return value


def the_puzzle(prices):
    stack_size = xxxcalc_stack_size(prices)
    outcomes = [
        "Splinter of Uul-Netol",
        "Splinter of Esh",
        "Splinter of Tul",
        "Splinter of Chayula",
        "Splinter of Xoph",
    ]
    splinters = [item for price in prices.values() for item in price if item["name"] in outcomes]
    values = [splinter["chaosValue"] for splinter in splinters]
    value = statistics.mean(values) / stack_size
    print(statistics.stdev(values) / stack_size)
    return value * 5


def emperors_luck(prices):
    stack_size = xxxcalc_stack_size(prices)
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
    value = sum(prices[key][0]["chaosValue"] for key, value in outcomes.items()) + 0.016
    return value / stack_size * 5


def the_bones(prices):
    stack_size = xxxcalc_stack_size(prices)
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    relevant_gems = [
        gem
        for gem in gems
        if "Vaal Summon Skeletons" in gem["name"]
        if gem["gemLevel"] == 21
        if gem.get("gemQuality") == None
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

    stack_size = xxxcalc_stack_size(prices)
    relevant_essences = [item for price in prices.values() for item in price if "Deafening Essence" in item["name"]]
    values = [essence["chaosValue"] for essence in relevant_essences]
    value = statistics.mean(values) / stack_size
    print(statistics.stdev(values) / stack_size)
    return value * 3


def the_tinkerers_table(prices):

    stack_size = xxxcalc_stack_size(prices)
    relevant_essences = [item for price in prices.values() for item in price if "Fossil" in item["name"]]
    values = [essence["chaosValue"] for essence in relevant_essences]
    value = statistics.mean(values) / stack_size
    print(statistics.stdev(values) / stack_size)
    return value * 5


def sambodhis_vow(prices):
    stack_size = xxxcalc_stack_size(prices)
    relevant = [item for price in prices.values() for item in price if "Mortal " in item["name"]]
    values = [item["chaosValue"] for item in relevant]
    value = statistics.mean(values) / stack_size
    print(statistics.stdev(values) / stack_size)
    return value


def the_primordial(prices):
    stack_size = xxxcalc_stack_size(prices)
    relevant = [item for price in prices.values() for item in price if item["name"].startswith("Primordial ")]
    values = [item["chaosValue"] for item in relevant]
    value = statistics.mean(values) / stack_size
    print(statistics.stdev(values) / stack_size)
    return value


def more_is_never_enough(prices):
    stack_size = xxxcalc_stack_size(prices)
    relevant = [
        item
        for price in prices.values()
        for item in price
        if item["name"].startswith("Gilded ")
        if item["name"].endswith("Scarab")
    ]
    values = [item["chaosValue"] for item in relevant]
    value = statistics.mean(values) / stack_size
    print(statistics.stdev(values) / stack_size)
    return value


def the_obscured(prices):
    stack_size = xxxcalc_stack_size(prices)
    relevant = [
        item
        for price in prices.values()
        for item in price
        if item["name"].endswith("Breachstone")
        if not any(q in item["name"] for q in ["nriched", "harged", "ure", "lawless"])
    ]
    values = [item["chaosValue"] for item in relevant]
    value = statistics.mean(values) / stack_size
    print(statistics.stdev(values) / stack_size)
    return value


def xxxcalc_stack_size(prices):
    div_card_name = inspect.stack()[1][3]
    stack_size = {name.lower().replace("'", "").replace(" ", "_"): value for name, value in prices.items()}[
        div_card_name
    ][0]["stackSize"]
    return stack_size
