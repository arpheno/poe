from poe.constants import LEAGUE
from .curr import ask_ninja_curr
from .item import ask_ninja_item
from .exchange import ask_ninja_exchange

EXCHANGE_TYPES = [
    "Currency",
    "Fragment",
    "DivinationCard",
    "Scarab",
    "Oil",
    "Fossil",
    "Resonator",
    "Essence",
    "DeliriumOrb",
    "Incubator",
    "Vial",
    "Artifact",
    "BlightedMap",
    "BlightRavagedMap",
    "UniqueMap",
    "Map",
    "Invitation",
    "Memory"
]

def asker(type):
    # Base data fetch
    if type in ["Fragment", "Currency"]:
        data = ask_ninja_curr(type, league=LEAGUE)
    else:
        data = ask_ninja_item(type, league=LEAGUE)
    
    # Enrich with Exchange data if applicable
    if type in EXCHANGE_TYPES:
        exchange_data = ask_ninja_exchange(type, league=LEAGUE)
        if exchange_data:
            print(f"Merging Exchange data for {type}...", end="")
            # Merge logic: Update chaosValue from exchange_data
            # data is dict: name -> list of items
            # exchange_data is dict: name -> list of items
            
            for name, items in data.items():
                if name in exchange_data:
                    # Assuming 1-to-1 mapping for most things, or taking the first match
                    # Exchange data usually has one entry per item type (except maybe for different stack sizes?)
                    # Item data might have multiple entries (e.g. different links, levels for gems - but gems are not in exchange)
                    
                    # For Divination Cards, Currency, etc., usually one entry per name.
                    ex_item = exchange_data[name][0]
                    ex_price = ex_item.get('chaosValue')
                    
                    if ex_price:
                        for item in items:
                            # Update price
                            # print(f"Updating {name}: {item.get('chaosValue')} -> {ex_price}")
                            item['chaosValue'] = ex_price
                            item['exchange_data'] = True # Flag to indicate source
            print("Done")
            
    return data
