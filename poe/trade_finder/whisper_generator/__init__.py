from math import ceil
from pathlib import Path

import numpy as np
from dataenforce import Dataset, validate
import pandas as pd

from poe.ninja import retrieve_prices
from poe.trade.exchange_resolver import ExchangeResolver
from poe.trade.listings_resolver import ListingsResolver


def query(want, minimum):
    return {
        "exchange": {
            "status": {"option": "online"},
            "have": ["chaos", "exalt"],
            "want": [want],
            "minimum": minimum,
        }
    }


def create_queries(df: Dataset["value":float, "expected_profit":float, ...], key_mapping, min_profit: float = 5):
    df = df.reset_index()
    print(f'Querying {df["index"][0]}', end=", ")
    df["minimum"] = np.ceil(min_profit / df.expected_profit)
    df["want"] = df["index"].map(key_mapping)
    df["query"] = df.apply(lambda x: query(x.want, x.minimum), axis=1)
    return df


def translate_currency(df, prices):
    df["pay_currency"] = df["pay_currency"].map({"chaos": "Chaos Orb", "exalted": "Exalted Orb"})
    currency_map = {k: v[0]["chaosValue"] for k, v in prices.items() if k in df.pay_currency.to_list()}
    df["chaos_price"] = df.price * df.pay_currency.map(currency_map)
    return df


def fill_in_whisper_amounts(whispers):
    whispers["profit"] = (whispers["value"] - whispers["chaos_price"]) * whispers.stock
    whispers["whisper"] = whispers.apply(
        lambda row: row["whisper_template"].format(row["stock"], row.price * row.stock), axis=1
    )
    whispers = whispers.query('chaos_price < value')
    print(f'Found {len(whispers)} results with {whispers["profit"].sum()} profit')
    print(whispers[['pay_currency','price','chaos_price']])
    return whispers


if __name__ == "__main__":
    prices = retrieve_prices(["Currency"])
    prices["Chaos Orb"] = [{"chaosValue": 1}]
    key_mapping = pd.read_csv(f"{Path(__file__).resolve().parent}/poe_keys.csv").set_index("name")["key"]
    reverse_mapping = {v: k for k, v in key_mapping.items()}
    s = pd.DataFrame(
        {
            "value": {"The Artist": 180.49},
            "expected_profit": {"The Artist": 130.49},
        }
    )
    df = s.reset_index()
    exchange_resolver = ExchangeResolver()
    listings_resolver = ListingsResolver()

    df = create_queries(df, key_mapping)
    # whispers = resolve_to_trades(df, exchange_resolver)

    df["trade_hash_json"] = df['query'].apply(exchange_resolver.resolve)
    whispers = pd.concat(df.trade_hash_json.apply(listings_resolver.resolve).values.tolist(), ignore_index=True)
    whispers["value"] = whispers.get_currency.map(reverse_mapping).map(s.value)
    whispers = translate_currency(whispers, prices)
    whispers = fill_in_whisper_amounts(whispers)
    print(whispers)
