from collections import Callable
from functools import partial

import pandas as pd

from poe.splinters.trades_resolver import resolve_to_trades


def splinter_profitability(
    completed_set_price: pd.Series, set_size: int, splinter_price: pd.Series, splinter_query: Callable
):
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
    df = splinters.reset_index().groupby("index").apply(partial(resolve_to_trades, splinter_query=splinter_query))
    return df
