from itertools import groupby

import pandas as pd

from poe.ninja import retrieve_prices


def scarab_orb_of_horizon(prices):
    orb_of_horizon_price = prices["Orb of Horizons"][0]["chaosValue"]
    prices = {k: v for k, v in prices.items() if " Scarab" in k}
    groups = list(
        (k, list(v))
        for k, v in groupby(sorted(prices.items()), key=lambda x: x[0].split()[0])
    )
    values = {
        key: {x[0].split()[1]: x[1][0]["chaosValue"] for x in values}
        for key, values in groups
    }
    df = pd.DataFrame(values).T
    df["mean"] = df.mean(axis=1)
    analysis = pd.concat(
        [
            profit_analysis(df, key, orb_of_horizon_price=orb_of_horizon_price)
            for key in df.keys()
        ]
    ).reset_index()
    analysis.columns = ["tier", "profitability", "profit", "kind", "price", "value"]
    analysis = analysis.query('kind != "mean"').set_index(["tier", "kind"])
    return analysis


def profit(df, key, orb_of_horizon_price):
    temp = df.drop(key, axis=1)
    return temp.mean(axis=1) / 2 - df[key] - orb_of_horizon_price / 2


def profitability(df, key, orb_of_horizon_price):
    temp = df.drop(key, axis=1)
    return (temp.mean(axis=1) / 2 - df[key] - orb_of_horizon_price / 2) / df[key]


def value(df, key):
    temp = df.drop(key, axis=1)
    return temp.mean(axis=1) / 2


def profit_analysis(df, key, orb_of_horizon_price):
    analysis = pd.concat(
        [
            profitability(df, key, orb_of_horizon_price),
            profit(df, key, orb_of_horizon_price),
        ],
        axis=1,
        keys=["profitability", "profit"],
    )
    analysis["kind"] = key
    analysis["price"] = df[key]
    analysis["value"] = value(df, key)
    return analysis


if __name__ == "__main__":
    prices = retrieve_prices(['Scarab','Currency'])
    analysis = scarab_orb_of_horizon(prices).sort_values(by="profit", ascending=False)
    print(analysis)
