import os
from poe.trade.proxy_search_resolver import SearchResolver
from poe.trade.proxy_listings_resolver import ListingsResolver
from poe.constants import LEAGUE

PROXY_BASE_URL = os.getenv("POE_PROXY_URL", "http://localhost:8999")

def get_doryani_institute_price():
    search_resolver = SearchResolver(league=LEAGUE, base_url=PROXY_BASE_URL)
    listings_resolver = ListingsResolver(league=LEAGUE, base_url=PROXY_BASE_URL)
    
    query = {
        "query": {
            "stats": [
                {
                    "filters": [
                        {
                            "disabled": False,
                            "id": "pseudo.pseudo_temple_gem_room_3",
                            "value": {
                                "option": 1
                            }
                        }
                    ],
                    "type": "and"
                }
            ],
            "status": {
                "option": "securable"
            }
        },
        "sort": {
            "price": "asc"
        }
    }
    
    try:
        print("Fetching Doryani's Institute price...")
        search_params = search_resolver.resolve(query)
        results = listings_resolver.resolve(search_params)
        
        prices = []
        for result in results.get('result', []):
            listing = result.get('listing', {})
            price = listing.get('price', {})
            currency = price.get('currency')
            amount = price.get('amount')
            
            if currency == 'chaos':
                prices.append(amount)
            elif currency == 'divine':
                # Fallback for divine, assuming 150c for now as per main.py
                prices.append(amount * 150) 
                
        if not prices:
            print("No prices found for Doryani's Institute")
            return 0
            
        avg_price = sum(prices) / len(prices)
        print(f"Average price for Doryani's Institute: {avg_price} chaos")
        return avg_price
        
    except Exception as e:
        print(f"Error fetching Doryani's Institute price: {e}")
        return 0

def get_vivid_watcher_price():
    search_resolver = SearchResolver(league=LEAGUE, base_url=PROXY_BASE_URL)
    listings_resolver = ListingsResolver(league=LEAGUE, base_url=PROXY_BASE_URL)
    
    query = {
        "query": {
            "stats": [
                {
                    "filters": [],
                    "type": "and"
                }
            ],
            "status": {
                "option": "securable"
            },
            "type": "Vivid Watcher"
        },
        "sort": {
            "price": "asc"
        }
    }
    
    try:
        print("Fetching Vivid Watcher price...")
        search_params = search_resolver.resolve(query)
        results = listings_resolver.resolve(search_params)
        
        prices = []
        for result in results.get('result', []):
            listing = result.get('listing', {})
            price = listing.get('price', {})
            currency = price.get('currency')
            amount = price.get('amount')
            
            if currency == 'chaos':
                prices.append(amount)
            elif currency == 'divine':
                prices.append(amount * 150) 
                
        if not prices:
            print("No prices found for Vivid Watcher")
            return 0
            
        avg_price = sum(prices) / len(prices)
        print(f"Average price for Vivid Watcher: {avg_price} chaos")
        return avg_price
        
    except Exception as e:
        print(f"Error fetching Vivid Watcher price: {e}")
        return 0

def get_wild_brambleback_price():
    search_resolver = SearchResolver(league=LEAGUE, base_url=PROXY_BASE_URL)
    listings_resolver = ListingsResolver(league=LEAGUE, base_url=PROXY_BASE_URL)
    
    query = {
        "query": {
            "stats": [
                {
                    "filters": [],
                    "type": "and"
                }
            ],
            "status": {
                "option": "securable"
            },
            "type": "Wild Brambleback"
        },
        "sort": {
            "price": "asc"
        }
    }
    
    try:
        print("Fetching Wild Brambleback price...")
        search_params = search_resolver.resolve(query)
        results = listings_resolver.resolve(search_params)
        
        prices = []
        for result in results.get('result', []):
            listing = result.get('listing', {})
            price = listing.get('price', {})
            currency = price.get('currency')
            amount = price.get('amount')
            
            if currency == 'chaos':
                prices.append(amount)
            elif currency == 'divine':
                prices.append(amount * 150) 
                
        if not prices:
            print("No prices found for Wild Brambleback")
            return 0
            
        avg_price = sum(prices) / len(prices)
        print(f"Average price for Wild Brambleback: {avg_price} chaos")
        return avg_price
        
    except Exception as e:
        print(f"Error fetching Wild Brambleback price: {e}")
        return 0
