import pandas as pd

from poe.ninja import retrieve_prices
from poe.valuation.splinters.domain.breach import breach_splinters
from poe.valuation.splinters.domain.simulacrum import simulacrum_splinters
from poe.valuation.splinters.domain.timeless import timeless_splinters


def splinter_values(prices):
    df = pd.concat(
        [
            breach_splinters(prices),
            timeless_splinters(prices),
            simulacrum_splinters(prices),
        ]
    )
    return df.to_dict()
if __name__ == '__main__':
    prices = retrieve_prices(["Fragment", "Currency"])
    result = splinter_values(prices)
    print(result)