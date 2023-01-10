from poe.ninja import retrieve_prices
import re


def fragment_sets(prices):
    sets = {}
    unrelenting = [item for key, item in prices.items() if "nrelenting" in key]
    timeless = [item for key, item in prices.items() if 'Emblem' in key if "imeless" in key if not "nrelenting" in key]
    shaper = [item for key, item in prices.items() if "Fragment of the" in key]
    elder = [prices['Fragment of Enslavement'], prices['Fragment of Constriction'], prices['Fragment of Purification'],
             prices['Fragment of Eradication']]
    uelder = [prices['Fragment of Knowledge'], prices['Fragment of Shape'], prices['Fragment of Terror'],
              prices['Fragment of Emptiness']]
    sirus = [item for key, item in prices.items() if "Crest" in key]
    assert len(elder) == 4
    assert len(uelder) == 4
    assert len(shaper) == 4
    assert len(unrelenting) == 5
    assert len(timeless) == 5
    assert len(sirus) == 4
    sets["unrelenting"] = sum(item[0]["chaosValue"] for item in unrelenting)
    sets["timeless"] = sum(item[0]["chaosValue"] for item in timeless)
    sets["shaper"] = sum(item[0]["chaosValue"] for item in shaper)
    sets["elder"] = sum(item[0]["chaosValue"] for item in elder)
    sets["uber_elder"] = sum(item[0]["chaosValue"] for item in uelder)
    sets["sirus"] = sum(item[0]["chaosValue"] for item in sirus)
    return sets


if __name__ == "__main__":
    prices = retrieve_prices(["Fragment"])
    result = fragment_sets(prices)
    print(result)
