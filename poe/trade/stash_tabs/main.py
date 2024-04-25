from collections import defaultdict
from pprint import pprint

from poe.trade.stash_tabs.caller import _call, stash_tab_api_interactor

if __name__ == "__main__":
    pprint(stash_tab_api_interactor(30))
# raw_items = get_some_tabs([22,23])
def retrieve_tab_mapping():
    raw_data = stash_tab_api_interactor(10)['tabs']
    base_name_to_id_mapping = {e['i']:e['n'] for e in raw_data}
    override_stash_tab_name = {e['i']:e['type'] for e in raw_data if e['type'] not in ['PremiumStash','QuadStash','NormalStash']}
    return {**base_name_to_id_mapping, **override_stash_tab_name}
def group_tab_mapping(tab_mapping):
    for key, value in tab_mapping.items():
        tabs = defaultdict(list)
        if '~price' in value:
            tabs['priced'].append(key)
            tabs['all'].append(key)
        elif 'Stash' in value:
            tabs['stash'].append(key)
            tabs['all'].append(key)
