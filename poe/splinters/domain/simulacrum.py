import pandas as pd

from poe.ninja import retrieve_prices
from poe.splinters.domain.splinter_info import SplinterInfo


def splinter_query(splinter: str):
    splinter_template = {
        "exchange": {
            "status": {"option": "online"},
            "have": ["chaos"],
            "want": [f"simulacrum-splinter"],
            "minimum": 30,
        }
    }
    return splinter_template


def simulacrum_splinters(prices):
    splinter_price = pd.Series(
        {key.split()[0]: value[0]["chaosValue"] for key, value in prices.items() if "Simulacrum Splinter" in key}
    )
    completed_set_price = pd.Series(
        {key: value[0]["chaosValue"] for key, value in prices.items() if key == "Simulacrum"}
    )
    return SplinterInfo(
        completed_set_price=completed_set_price,
        splinter_price=splinter_price,
        set_size=300,
        splinter_query=splinter_query,
    )
