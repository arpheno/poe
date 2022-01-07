import logging

import pandas as pd

from poe.trade.query_resolver import resolve_exchange
from poe.trade_finder.whisper_generator.listings_resolver import resolve_listings

min_profit = 5
logger = logging.getLogger(__name__)
default_return = pd.DataFrame(
    columns=["pay_currency", "get_currency", "price", "stock", "id", "whisper_template", "value", "profit", "whisper"]
)


def resolve_to_trades(splinter: pd.DataFrame):
    series = splinter.iloc[0]
    try:
        hash, result = resolve_exchange(series["query"])
    except Exception as e:
        logger.exception("Something not ok")
        return default_return

    df = resolve_listings(hash, result)
    if not len(df):
        return default_return
    df = df[df.price < series["value"]]
    if not len(df):
        return default_return
    df["value"] = series.value
    df["profit"] = (df["value"] - df["price"]) * df.stock
    df["whisper"] = df.apply(
        lambda row: row["whisper_template"].format(row["stock"], row.price * row.stock), axis=1
    )
    return df
