from poe.ninja import retrieve_prices
import re


def fragment_sets(prices):
    sets = {}
    sets["unrelenting"] = sum(
        item[0]["chaosValue"] for key, item in prices.items() if "nrelenting" in key
    )
    sets["timeless"] = sum(
        item[0]["chaosValue"]
        for key, item in prices.items()
        if "imeless" in key
        if not "nrelenting" in key
    )
    return sets


if __name__ == "__main__":
    prices = retrieve_prices(["Fragment"])
    result = fragment_sets(prices)
    print(result)
