import pandas as pd


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
    completed_set_price = pd.Series(
        {
            " ".join(key.split()[1:-1]): value[0]["chaosValue"]
            for key, value in prices.items()
            if "Emblem" in key
            if "Timeless" in key
            if not "relenting" in key
        }
    )
    set_size = 100
    value = completed_set_price / set_size
    value.index = "Timeless " + value.index + " Splinter"
    value.index = value.index.str.replace("Eternal", "Eternal Empire")
    return value
