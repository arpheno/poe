import pandas as pd

from poe.splinters.domain.splinter_info import SplinterInfo


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


def timeless_splinters(prices):
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
    return SplinterInfo(
        completed_set_price=completed_set_price,
        splinter_price=splinter_price,
        set_size=100,
        splinter_query=splinter_query,
    )
