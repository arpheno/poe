from poe.item.item_factory import item_factory
from poe.trade.stash_tabs.caller import _call
from poe.type_determiner import determine_type


def get_all_tabs(mapping:tuple[str]):
    all_items = []
    for tab_index in range(20):
        stashtab, data = _call(tab_index)
        for item in data:
            item["name"] = item["typeLine"]
            item_type = determine_type(item, mapping)
            if not item_type:
                print(f"Could not find an item type for {item['name']}")
                continue
            try:
                new_item = item_factory(stashtab=stashtab, **item, type=item_type, )
                all_items.append(new_item)
            except:
                print(f"Couldn't add item {item['name']}")
    return all_items