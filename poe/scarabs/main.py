from itertools import groupby
import pandas as pd
from poe.ninja import retrieve_prices


def profit(df, key):
    temp = df.drop(key, axis=1)
    return temp.mean(axis=1)/2 - df[key]


def profitability(df, key):
    temp = df.drop(key, axis=1)
    return (temp.mean(axis=1)/2 - df[key] ) / df[key]


def value(df, key):
    temp = df.drop(key, axis=1)
    return temp.mean(axis=1) /2


def profit_analysis(df, key):
    analysis = pd.concat([profitability(df, key), profit(df, key)], axis=1, keys=["profitability", "profit"])
    analysis["kind"] = key
    analysis["price"] = df[key]
    analysis["value"] = value(df, key)
    return analysis


def scarab_orb_of_horizon():
    prices = retrieve_prices(["Scarab"])
    groups = groupby(sorted(prices.items()), key=lambda x: x[0].split()[0])
    values = {key: {x[0].split()[1]: x[1][0]["chaosValue"] for x in values} for key, values in groups}
    df = pd.DataFrame(values).T
    df = df.drop("Lure", axis=1)
    df = df.drop("Craicic").drop("Farric").drop("Fenumal").drop("Saqawine")
    df["mean"] = df.mean(axis=1)
    analysis = pd.concat([profit_analysis(df, key) for key in df.keys()]).reset_index()
    analysis.columns = ["tier", "profitability", "profit", "kind",'price','value']
    analysis = analysis.set_index(["tier", "kind"])
    return analysis


if __name__ == "__main__":
    analysis = scarab_orb_of_horizon().sort_values(by="profit", ascending=False)
    print(analysis)
