from constants import LEAGUE
from poe.trade.listings_resolver import ListingsResolver
from poe.trade.search_resolver import SearchResolver

if __name__ == '__main__':
    query = {
        "query": {
            "status": {
                "option": "online"
            },
            "name": "Forbidden Shako",
            "type": "Great Crown",
            "stats": [
                {
                    "type": "and",
                    "filters": [],
                    "disabled": False
                }
            ]
        },
        "sort": {
            "price": "asc"
        }
    }
    search_resolver = SearchResolver(league=LEAGUE)
    listings_resolver = ListingsResolver(league=LEAGUE)
    temp = listings_resolver.resolve(search_resolver.resolve(query))
    result = temp
