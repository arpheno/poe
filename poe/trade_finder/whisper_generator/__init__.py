from math import ceil
from pathlib import Path

from dataenforce import Dataset, validate
import pandas as pd

from poe.trade_finder.whisper_generator.trades_resolver import resolve_to_trades


def query(want, minimum):
    return {
        "exchange": {
            "status": {"option": "online"},
            "have": ["chaos"],
            "want": [want],
            "minimum": minimum,
        }
    }


def generate_whispers(df: Dataset["value":float, "expected_profit":float, ...], min_profit: float = 5):
    df = df.reset_index()
    key_mapping = pd.read_csv(f"{Path(__file__).resolve().parent}/poe_keys.csv").set_index("name")["key"]
    print(f'Querying {df["index"][0]}',end=', ')
    df["minimum"] = ceil(min_profit / df.expected_profit)
    df["want"] = df["index"].map(key_mapping)
    df["query"] = df.apply(lambda x: query(x.want, x.minimum), axis=1)
    result = resolve_to_trades(df)
    print(f'Found {len(result)} results with {result["profit"].sum()} profit')
    return result


if __name__ == "__main__":
    s = pd.DataFrame({"value": {"Splinter of Uul-Netol": 1.0}, "expected_profit": {"Splinter of Uul-Netol": 5.0}})
    df = s.reset_index()
    whispers = generate_whispers(df)
    print(whispers)
