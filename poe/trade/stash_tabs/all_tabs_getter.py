from poe.constants import LEAGUE
from poe.trade.stash_tabs.stash_tab_api import StashTabAPI


def add_stashtab_to_item_info(data, tab_index):
    # Items from the stash tab API do not have the stash tab name as a field.
    # This function retrieves the stash tab name and adds it to the item info.
    tabs = data["tabs"]
    [current_tab] = [tab for tab in tabs if tab["i"] == tab_index]
    current_tab_name = current_tab["n"]
    for item in data["items"]:
        item["stashtab"] = current_tab_name
    return data

#Deprecated usage of DEFAULT_STASH_TAB_API, remove when possible
DEFAULT_STASH_TAB_API= StashTabAPI('swozn', LEAGUE, base_url="http://localhost:8999")
def get_some_tabs(tab_indices: list[int] = [], stash_tab_api: StashTabAPI = DEFAULT_STASH_TAB_API):
    all_items = []
    for tab_index in tab_indices:
        data = stash_tab_api.fetch_tab_data(tab_index)
        processed_data = add_stashtab_to_item_info(data, tab_index)
        all_items.extend(processed_data['items'])
    return all_items

