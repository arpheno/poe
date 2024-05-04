# Standard library imports
import requests

# Third party imports
import pandas as pd

from constants import LEAGUE
# Local application imports
from poe.item.newitems.base_item_model import Item
from poe.trade.headers import headers
from trade.stash_tabs.all_tabs_getter import get_some_tabs
from trade.stash_tabs.stash_tab_api import StashTabAPI
from trade.stash_tabs.stash_tab_mapping_creator import TabMapper, retrieve_tab_mapping
from woke.mod_mapper import ModMapper

# Pandas settings
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

if __name__ == '__main__':
    stash_tab_api = StashTabAPI('swozn', LEAGUE, base_url="http://localhost:8999")
    mapper = TabMapper()
    tabs = retrieve_tab_mapping(mapper,stash_tab_api=stash_tab_api)
    selected_tabs = tabs['empty']
    raw_items = get_some_tabs(list(selected_tabs))
    trade_keys = requests.get('http://localhost:8999/api/trade/data/stats', headers=headers).json()
    mod_mapper = ModMapper(trade_keys)
    item = Item(**raw_items[0])
    print(mod_mapper.map_mods('explicit', item.explicitMods))
    print(mod_mapper.map_mods('implicit', item.implicitMods))
