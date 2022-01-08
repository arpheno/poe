from poe.ninja import retrieve_prices
from poe.trade_finder.profitable_items_finder import find_profitable_items
from poe.trade_finder.whisper_generator import generate_whispers



def generate_whisper(df):
    result = df.reset_index().groupby("index").apply(generate_whispers)
    return result


if __name__ == "__main__":
    prices = retrieve_prices()
    df= find_profitable_items(prices)
    whispers=generate_whisper(df)
    print(whispers)
