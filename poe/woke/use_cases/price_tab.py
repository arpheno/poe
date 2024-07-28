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


def price_tab(tab_name='empty'):
    stash_tab_api = StashTabAPI('swozn', LEAGUE, base_url="http://localhost:8999")
    search_resolver = SearchResolver(league=LEAGUE, base_url="http://localhost:8999")
    listings_resolver = ListingsResolver(league=LEAGUE, base_url="http://localhost:8999")
    trade_keys = requests.get('http://localhost:8999/api/trade/data/stats', headers=headers).json()
    mod_mapper = ModMapper(trade_keys)
    mapper = TabMapper()
    tabs = retrieve_tab_mapping(mapper, stash_tab_api=stash_tab_api)
    selected_tabs = tabs[tab_name]
    raw_items = get_some_tabs(list(selected_tabs))
    item = Item(**raw_items[0])
    mods = {
        'explicits': mod_mapper.map_mods('explicit', item.explicitMods),
        'implicits': mod_mapper.map_mods('implicit', item.implicitMods)
    }
    query = build_query(mods)
    params = search_resolver.resolve(query)
    result = listings_resolver.resolve(params)
    # What's still missing here is using the obtained search results to suggest a price for the item
    return result
