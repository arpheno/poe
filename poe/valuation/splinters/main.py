from poe.ninja import retrieve_prices
from poe.trade_finder.whisper_generator import generate_whispers


def main(prices):
    df['expected_profit'] = df.value - df.price
    df = df[df.expected_profit > 0]
    df = df.reset_index().groupby("index").apply(generate_whispers)
    return df


if __name__ == "__main__":
    prices = retrieve_prices(["Fragment", "Currency"])
    result=main(prices)
    print(result)
