from poe.item.item_factory import item_factory
from poe.trade.stash_tabs.caller import _call
from poe.type_determiner import determine_type


def get_all_tabs(num_tabs:int=20):#TODO THIS SHOULD NOT BE HARDCODED
    all_items = []
    for tab_index in range(num_tabs):
        data = _call(tab_index)
        all_items.extend(data)
    return all_items