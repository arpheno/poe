import pandas as pd

from poe.ninja import retrieve_prices
from poe.trade.query_resolver import resolve_exchange


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


def timeless_profitability():
    prices = retrieve_prices(["Fragment"])
    splinters = pd.Series(
        {
            key.replace("Timeless", "").replace("Splinter", "").strip(): value[0]["chaosValue"]
            for key, value in prices.items()
            if "Splinter" in key
            if "Timeless" in key
        }
    )
    emblems = pd.Series(
        {
            key.replace("Timeless", "").replace("Emblem", "").strip(): value[0]["chaosValue"]
            for key, value in prices.items()
            if "Emblem" in key
            if not "relenting" in key
        }
    )

    profitable_splinters: pd.Series = (emblems / 100 - splinters).where(lambda x: x > 0).dropna()
    print(profitable_splinters)
    print(profitable_splinters)
    for key in profitable_splinters.keys():
        #TODO: Adjust trade query for profit/trade
        print(f'Buy {key} between {splinters[key]} and {splinters[key]+profitable_splinters[key]}')
        hash = resolve_exchange(splinter_query(key))
    profitable_splinters = profitable_splinters.rename(
        {x: f"Timeless {x} Splinter" for x in profitable_splinters.keys()}
    )
    return profitable_splinters


if __name__ == "__main__":
    timeless_profitability()
