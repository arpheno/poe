import logging

import pandas as pd

from poe.ninja import retrieve_prices
from poe.splinters.splinter_profiter import splinter_profitability



def splinter_query(splinter: str):
    splinter_template = {
        "exchange": {
            "status": {"option": "online"},
            "have": ["chaos"],
            "want": [f"timeless-{splinter.lower()}-splinter"],
            "minimum": 30,
        }
    }
    return splinter_template


def timeless_splinters(
        set_size=100
):
    prices = retrieve_prices(["Fragment"])
    splinter_price = pd.Series(
        {
            key.split()[1]: value[0]["chaosValue"]
            for key, value in prices.items()
            if "Splinter" in key
            if "Timeless" in key
        }
    )
    completed_set_price = pd.Series(
        {
            key.split()[1]: value[0]["chaosValue"]
            for key, value in prices.items()
            if "Emblem" in key
            if not "relenting" in key
        }
    )
    df = splinter_profitability(completed_set_price, set_size, splinter_price,splinter_query=splinter_query)
    print(df)
    return df


if __name__ == "__main__":
    timeless_splinters()
