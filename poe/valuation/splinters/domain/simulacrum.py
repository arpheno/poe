import pandas as pd


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
    completed_set_price = pd.Series(
        {key: value[0]["chaosValue"] for key, value in prices.items() if key == "Simulacrum"}
    )
    set_size = 300
    value= completed_set_price / set_size
    value.index = ['Simulacrum Splinter']
    return value