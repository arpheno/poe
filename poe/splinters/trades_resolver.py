import pandas as pd

from poe.splinters.listings_resolver import resolve_listings
from poe.trade.query_resolver import resolve_exchange


def resolve_to_trades(splinter: pd.DataFrame,splinter_query):
    series = splinter.iloc[0]
    hash, result = resolve_exchange(splinter_query(series['index']))
    df = resolve_listings(hash, result)
    df = df[df.price < series['value']]
    df['value'] = series.value
    df["profit"] = (df['value'] - df['price']) * df.stock
    df['whisper'] = df.apply(lambda row:row['whisper_template'].format(row['stock'],row.price*row.stock),axis=1)
    return df