from poe.ninja import retrieve_prices
from poe.trade_finder.profitable_items_finder import find_profitable_items
from poe.trade_finder.whisper_generator import create_queries



def generate_whisper(df):
    result = df.reset_index().groupby("index").apply(create_queries)
    return result


if __name__ == "__main__":
    prices = retrieve_prices()
    df= find_profitable_items(prices).rename_axis(index='index')
    whispers=generate_whisper(df)
    print(whispers)
