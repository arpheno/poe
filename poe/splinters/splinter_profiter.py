
import pandas as pd


def splinter_profitability(completed_set_price: pd.Series, set_size: int, splinter_price: pd.Series):
    splinters = pd.concat(
        [
            splinter_price,
            completed_set_price,
        ],
        axis=1,
        keys=["price", "completed_set_price"],
    )
    splinters["value"] = splinters.completed_set_price / set_size
    splinters["profit"] = splinters.value - splinters.price
    splinters = splinters[splinters.profit > 0]
    return splinters
