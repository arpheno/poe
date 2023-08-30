import sys
import pprint

sys.path.append("/home/dhokuav/poe")  # Replace 'path_to_subfolder' with the actual path

from poe.ninja import retrieve_prices
from poe.temple.ascension import ascension_rules


def ascension_values(prices):
    valuations = {}
    for name, func in ascension_rules.items():
        try:
            valuations[name] = func(prices)
        except ValueError:
            pass
    return {**valuations}


if __name__ == "__main__":
    prices = retrieve_prices()
    pprint.pprint(ascension_values(prices))
