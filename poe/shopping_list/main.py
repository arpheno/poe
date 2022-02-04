import pandas as pd

from poe.shopping_list import queries
from poe.trade.exchange_resolver import ExchangeResolver
from poe.trade.listings_resolver import ListingsResolver
from poe.trade.search_resolver import SearchResolver


def main():
    df = pd.Series(queries.q)

    listings_resolver = ListingsResolver(league='standard')
    search_resolver = SearchResolver(league='standard')


    whispers_stacked = df.apply(search_resolver.resolve).apply(listings_resolver.resolve)
    print(whispers_stacked)

if __name__ == "__main__":
    main()
