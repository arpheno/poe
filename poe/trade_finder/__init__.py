from poe.ninja import retrieve_prices
from poe.trade_finder.whisper_generator import generate_whispers
from poe.valuation import own_valuations

max_invest = 40
import pandas as pd

if __name__ == "__main__":
    prices = retrieve_prices()
    values = own_valuations(prices)
    df = pd.DataFrame()
    df["value"] = pd.Series(values).dropna()
    df["price"] = df.index.map(lambda x: prices[x][0]["chaosValue"])
    df["expected_profit"] = df.value - df.price
    df = df[df.expected_profit > 0.2].sort_values("expected_profit", ascending=False)
    df = df.query(f"price< {max_invest}")
    df = df.reset_index().groupby("index").apply(generate_whispers)
    print(df)
