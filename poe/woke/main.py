import requests
import pandas as pd
import bs4
from poe.trade.headers import headers
import difflib
from pprint import pprint

from trade.stash_tabs.all_tabs_getter import get_some_tabs
from trade.stash_tabs.stash_tab_mapping_creator import TabMapper, retrieve_tab_mapping

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
import re
from poe.valuation.framework.tft_adapter.adapter import TftAdapter
from poe.valuation.framework.compass_name_matcher import find_matches

trade_keys = requests.get('https://www.pathofexile.com/api/trade/data/stats', headers=headers).json()
mod_mapping = pd.DataFrame(
    [item for items in pd.DataFrame(pd.DataFrame(trade_keys['result'])['entries'])['entries'].tolist() for item in
     items])
mod_mapping['text'] = mod_mapping['text']
mapper = TabMapper()
tabs = retrieve_tab_mapping(mapper)
selected_tabs = tabs['empty']
raw_items = get_some_tabs(list(selected_tabs))
raw_items
