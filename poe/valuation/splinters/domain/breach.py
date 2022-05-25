import pandas as pd


def splinter_query(splinter: str):
    splinter_template = {
        "exchange": {
            "status": {"option": "online"},
            "have": ["chaos"],
            "want": [splinter],
            "minimum": 30,
        }
    }
    return splinter_template


def breach_splinters(prices):
    completed_set_price = pd.Series(
        {
            key.split("'")[0]: value[0]["chaosValue"]
            for key, value in prices.items()
            if "'s Breachstone" in key
        }
    )
    set_size = 100
    value = completed_set_price / set_size
    value.index = "Splinter of " + value.index
    return value
