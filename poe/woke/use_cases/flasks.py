import random
from itertools import product
from pprint import pprint

import requests

from constants import LEAGUE
from item.newitems.base_item_model import Item
from trade.headers import headers
from trade.proxy_listings_resolver import ListingsResolver
from trade.proxy_search_resolver import SearchResolver
from trade.stash_tabs.all_tabs_getter import get_some_tabs
from trade.stash_tabs.stash_tab_api import StashTabAPI
from trade.stash_tabs.stash_tab_mapping_creator import TabMapper, retrieve_tab_mapping
from woke.mod_mapper import ModMapper
from woke.query_builder import build_query


class ItemSearcher:
    def __init__(self, search_resolver: SearchResolver, listings_resolver: ListingsResolver):
        self.search_resolver = search_resolver
        self.listings_resolver = listings_resolver

    def search(self, query_args):
        query = build_query(**query_args)
        params = self.search_resolver.resolve(query)
        result = self.listings_resolver.resolve(params)
        return result
# Define a function to shuffle a list and return it
def shuffle_list(lst):
    shuffled_lst = list(lst).copy()
    random.shuffle(shuffled_lst)
    return shuffled_lst

def flasks():
    search_resolver = SearchResolver(league=LEAGUE, base_url="http://localhost:8999")
    listings_resolver = ListingsResolver(league=LEAGUE, base_url="http://localhost:8999")
    item_searcher = ItemSearcher(search_resolver, listings_resolver)
    trade_keys = requests.get('http://localhost:8999/api/trade/data/stats', headers=headers).json()
    mod_mapper = ModMapper(trade_keys)
    misc = {'filters': {
        "corrupted": {
            "option": "false"
        },
        "quality": {
            "min": 20,
            "max": 20
        }
    }}
    result = {}
    prefixes = [
        '25% increased effect',
        '31% chance to gain a Flask Charge when you deal a Critical Strike'
    ]
    suffixes = [
        '61% reduced Effect of Curses on you during Effect',
        '56% increased Armour during Effect',
        '56% increased Evasion Rating during Effect',
        '15% increased Attack Speed during Effect',
        '15% increased Cast Speed during Effect',
        '12% increased Movement Speed during Effect',
        '18% additional Elemental Resistances during Effect',
        '50% increased Critical Strike Chance during Effect',
        '51% Chance to Avoid being Stunned during Effect',
    ]
    flask_types = ['Sapphire Flask', 'Ruby Flask', 'Topaz Flask','Granite Flask','Quicksilver Flask','Silver Flask','Amethyst Flask','Jade Flask','Diamond Flask']
    for flask_type,prefix, suffix in shuffle_list(product(flask_types, prefixes, suffixes)):
        print(f'Processing {flask_type} with {prefix} and {suffix}')
        args = {
            'mods': mod_mapper.map_mods('explicit', [prefix, suffix]),
            'type': flask_type,
            'misc': misc}
        result[(flask_type, prefix,suffix)] = item_searcher.search(args)

    # What's still missing here is using the obtained search results to suggest a price for the item
    return result


import pandas as pd
def to_chaos(price:dict):
    multiplier = 1 if price['currency'] == 'chaos' else 100
    return price['amount'] * multiplier
if __name__ == '__main__':
    matches = flasks()
    # I need a funciton like extract but from the final value which is a dict,i  need to strip the "type" key
    extract = lambda x: x['listing']['price']
    matches = {flask_type: [extract(m) for m in match.get('result',[])] for flask_type, match in matches.items()}

    matches = {flask_type: [to_chaos(price) for price in prices] for flask_type, prices in matches.items()}
    pprint(matches)
