import sys

sys.path.append("/home/dhokuav/poe")  # Replace 'path_to_subfolder' with the actual path

from poe.ninja import retrieve_prices

prices = retrieve_prices()

ascension_values = {}


def apeps_supremacy(prices):
    vial = [
        item
        for price in prices.values()
        for item in price
        if "Vial of Awakening" in item["name"]
    ]
    reagent = [
        item
        for price in prices.values()
        for item in price
        if "Apep's Slumber" in item["name"]
    ]
    result = [
        item
        for price in prices.values()
        for item in price
        if "Apep's Supremacy" in item["name"]
    ]
    values = [item["chaosValue"] for item in vial + reagent + result]
    value = values[2] - (values[0] + values[1])
    return (
        vial[0]["name"],
        values[0],
        reagent[0]["name"],
        values[1],
        result[0]["name"],
        value,
    )


def cowards_legacy(prices):
    vial = [
        item
        for price in prices.values()
        for item in price
        if "Vial of Consequence" in item["name"]
    ]
    reagent = [
        item
        for price in prices.values()
        for item in price
        if "Coward's Chains" in item["name"]
    ]
    result = [
        item
        for price in prices.values()
        for item in price
        if "Coward's Legacy" in item["name"]
    ]
    values = [item["chaosValue"] for item in vial + reagent + result]
    value = values[2] - (values[0] + values[1])
    return (
        vial[0]["name"],
        values[0],
        reagent[0]["name"],
        values[1],
        result[0]["name"],
        value,
    )


def slavedrivers_hand(prices):
    vial = [
        item
        for price in prices.values()
        for item in price
        if "Vial of Dominance" in item["name"]
    ]
    reagent = [
        item
        for price in prices.values()
        for item in price
        if "Architect's Hand" in item["name"]
    ]
    result = [
        item
        for price in prices.values()
        for item in price
        if "Slavedriver's Hand" in item["name"]
    ]
    values = [item["chaosValue"] for item in vial + reagent + result]
    value = values[2] - (values[0] + values[1])
    return (
        vial[0]["name"],
        values[0],
        reagent[0]["name"],
        values[1],
        result[0]["name"],
        value,
    )


def fate_of_the_vaal(prices):
    vial = [
        item
        for price in prices.values()
        for item in price
        if "Vial of Fate" in item["name"]
    ]
    reagent = [
        item
        for price in prices.values()
        for item in price
        if "Story of the Vaal" in item["name"]
    ]
    result = [
        item
        for price in prices.values()
        for item in price
        if "Fate of the Vaal" in item["name"]
    ]
    values = [item["chaosValue"] for item in vial + reagent + result]
    value = values[2] - (values[0] + values[1])
    return (
        vial[0]["name"],
        values[0],
        reagent[0]["name"],
        values[1],
        result[0]["name"],
        value,
    )


def mask_of_the_stiched_demon(prices):
    vial = [
        item
        for price in prices.values()
        for item in price
        if "Vial of Summoning" in item["name"]
    ]
    reagent = [
        item
        for price in prices.values()
        for item in price
        if "Mask of the Spirit Drinker" in item["name"]
    ]
    result = [
        item
        for price in prices.values()
        for item in price
        if "Mask of the Stitched Demon" in item["name"]
    ]
    values = [item["chaosValue"] for item in vial + reagent + result]
    value = values[2] - (values[0] + values[1])
    return (
        vial[0]["name"],
        values[0],
        reagent[0]["name"],
        values[1],
        result[0]["name"],
        value,
    )


def omeyocan(prices):
    vial = [
        item
        for price in prices.values()
        for item in price
        if "Vial of the Ritual" in item["name"]
    ]
    reagent = [
        item
        for price in prices.values()
        for item in price
        if "Dance of the Offered" in item["name"]
    ]
    result = [
        item
        for price in prices.values()
        for item in price
        if "Omeyocan" in item["name"]
    ]
    values = [item["chaosValue"] for item in vial + reagent + result]
    value = values[2] - (values[0] + values[1])
    return (
        vial[0]["name"],
        values[0],
        reagent[0]["name"],
        values[1],
        result[0]["name"],
        value,
    )


def transcendent_flesh(prices):
    vial = [
        item
        for price in prices.values()
        for item in price
        if "Vial of Transcendence" in item["name"]
    ]
    reagent = [
        item
        for price in prices.values()
        for item in price
        if "Tempered Flesh" in item["name"]
    ]
    result = [
        item
        for price in prices.values()
        for item in price
        if "Transcendent Flesh" in item["name"]
    ]
    values = [item["chaosValue"] for item in vial + reagent + result]
    value = values[2] - (values[0] + values[1])
    return (
        vial[0]["name"],
        values[0],
        reagent[0]["name"],
        values[1],
        result[0]["name"],
        value,
    )


def transcendent_spirit(prices):
    vial = [
        item
        for price in prices.values()
        for item in price
        if "Vial of Transcendence" in item["name"]
    ]
    reagent = [
        item
        for price in prices.values()
        for item in price
        if "Tempered Spirit" in item["name"]
    ]
    result = [
        item
        for price in prices.values()
        for item in price
        if "Transcendent Spirit" in item["name"]
    ]
    values = [item["chaosValue"] for item in vial + reagent + result]
    value = values[2] - (values[0] + values[1])
    return (
        vial[0]["name"],
        values[0],
        reagent[0]["name"],
        values[1],
        result[0]["name"],
        value,
    )


def transcendent_mind(prices):
    vial = [
        item
        for price in prices.values()
        for item in price
        if "Vial of Transcendence" in item["name"]
    ]
    reagent = [
        item
        for price in prices.values()
        for item in price
        if "Tempered Mind" in item["name"]
    ]
    result = [
        item
        for price in prices.values()
        for item in price
        if "Transcendent Mind" in item["name"]
    ]
    values = [item["chaosValue"] for item in vial + reagent + result]
    value = values[2] - (values[0] + values[1])
    return (
        vial[0]["name"],
        values[0],
        reagent[0]["name"],
        values[1],
        result[0]["name"],
        value,
    )


def zerphis_heart(prices):
    vial = [
        item
        for price in prices.values()
        for item in price
        if "Vial of Sacrifice" in item["name"]
    ]
    reagent = [
        item
        for price in prices.values()
        for item in price
        if "Sacrificial Heart" in item["name"]
    ]
    result = [
        item
        for price in prices.values()
        for item in price
        if "Zerphi's Heart" in item["name"]
    ]
    values = [item["chaosValue"] for item in vial + reagent + result]
    value = values[2] - (values[0] + values[1])
    return (
        vial[0]["name"],
        values[0],
        reagent[0]["name"],
        values[1],
        result[0]["name"],
        value,
    )


def soul_ripper(prices):
    vial = [
        item
        for price in prices.values()
        for item in price
        if "Vial of the Ghost" in item["name"]
    ]
    reagent = [
        item
        for price in prices.values()
        for item in price
        if "Soul Catcher" in item["name"]
    ]
    result = [
        item
        for price in prices.values()
        for item in price
        if "Soul Ripper" in item["name"]
    ]
    values = [item["chaosValue"] for item in vial + reagent + result]
    value = values[2] - (values[0] + values[1])
    return (
        vial[0]["name"],
        values[0],
        reagent[0]["name"],
        values[1],
        result[0]["name"],
        value,
    )


ascension_values["Apep's Supremacy"] = apeps_supremacy
ascension_values["Coward's Legacy"] = cowards_legacy
ascension_values["Slavedriver's Hand"] = slavedrivers_hand
ascension_values["Fate of the Vaal"] = fate_of_the_vaal
ascension_values["Mask of the Stitched Demon"] = mask_of_the_stiched_demon
ascension_values["Omeyocan"] = omeyocan
ascension_values["Transcendent Flesh"] = transcendent_flesh
ascension_values["Transcendent Spirit"] = transcendent_spirit
ascension_values["Transcendent Mind"] = transcendent_mind
ascension_values["Zerphi's Heart"] = zerphis_heart
ascension_values["Soul Ripper"] = soul_ripper

for function_name in ascension_values:
    if function_name in ascension_values:
        function_to_call = ascension_values[function_name]
        result = function_to_call(prices)  # Call the function
        print(f"Result of {function_name}: {result}")
    else:
        print(f"Function '{function_name}' not found in the ascension_values dictionary.")