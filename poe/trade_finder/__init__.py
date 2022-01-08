from poe.ninja import retrieve_prices
from poe.trade_finder.profitable_items_finder import find_profitable_items
from poe.trade_finder.whisper_generator import generate_whispers

max_invest = 40


def generate_whispers(df):
    df = df.query(f"price< {max_invest}")
    result = df.reset_index().groupby("index").apply(generate_whispers)
    return result


if __name__ == "__main__":
    prices = retrieve_prices()
    df= find_profitable_items(prices)
    whispers=generate_whispers(df)
    print(whispers)
