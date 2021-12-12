import pandas as pd

from poe.ninja import retrieve_prices
from poe.splinters.domain.breach import breach_splinters
from poe.splinters.domain.simulacrum import simulacrum_splinters
from poe.splinters.domain.timeless import timeless_splinters
from poe.splinters.profit_finder import find_profit_in_splinters

def main():
    prices = retrieve_prices(["Fragment", "Currency"])
    splinters = {
        "breach": breach_splinters(prices),
        "timeless": timeless_splinters(prices),
        "simulacrum": simulacrum_splinters(prices),
    }
    result = all_trades = pd.concat(
        [find_profit_in_splinters(splinter_info) for splinter, splinter_info in splinters.items()])
    print(result)
    return result
if __name__ == "__main__":
    main()