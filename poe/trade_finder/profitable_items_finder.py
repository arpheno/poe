import pandas as pd

from poe.ninja import retrieve_prices
from poe.valuation import own_valuations


def find_profitable_items(prices, values):
    df = pd.DataFrame()
    df["value"] = pd.Series(values).dropna()
    df["price"] = df.index.map(lambda x: prices[x][0]["chaosValue"])
    df["expected_profit"] = df.value - df.price
    df = df[df.expected_profit > 0].sort_values("expected_profit", ascending=False)
    df = df.rename_axis(index="name")
    return df


if __name__ == "__main__":
    prices = retrieve_prices()
    values = own_valuations(prices)
    items = find_profitable_items(prices, values)

    items["icon"] = items.index.map(lambda x: prices[x][0].get("icon", ""))
    print(items)
