from functools import partial

import pandas as pd

from poe.ninja import retrieve_prices
from poe.splinters.domain.splinter_info import SplinterInfo
from poe.splinters.splinter_profiter import splinter_profitability
from poe.splinters.trades_resolver import resolve_to_trades


def splinter_query(splinter: str):
    splinter_template = {
        "exchange": {
            "status": {"option": "online"},
            "have": ["chaos"],
            "want": [f"splinter-{splinter.lower()}"],
            "minimum": 30,
        }
    }
    return splinter_template


def breach_splinters(prices):
    splinter_price = pd.Series(
        {key.split()[-1]: value[0]["chaosValue"] for key, value in prices.items() if "Splinter of" in key}
    )
    completed_set_price = pd.Series(
        {key.split("'")[0]: value[0]["chaosValue"] for key, value in prices.items() if "'s Breachstone" in key}
    )

    return SplinterInfo(
        completed_set_price=completed_set_price,
        splinter_price=splinter_price,
        set_size=100,
        splinter_query=splinter_query,
    )
