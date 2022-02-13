from typing import Callable

from constants import blacklist
from poe.item.item_factory import item_factory
from poe.ninja import retrieve_prices
from poe.trade.stash_tabs.all_tabs_getter import get_all_tabs
from poe.item.type_determiner import type_mapping


def build_items(prices, type_mapper: Callable):
    items = get_all_tabs(20)
    types = map(type_mapper, items)
    items = [
        {"type": t, **item}
        for item, t in zip(items, types)
        if not item["typeLine"] in blacklist
        if not item["stashtab"] == "noindex"
    ]
    all_items = []
    for old_item in items:
        if not old_item["type"]:
            print(f"Could not find an item type for {old_item['typeLine']}")
            continue
        if old_item['type']in {'Base'}:
            continue
        if old_item['type']in {'Heist','Expedition','Watchstone','Organ','CurrencyShard'}:
            continue
        if old_item['type'] in ['ClusterJewel']:
            print('hi')
        item = item_factory(**old_item)
        item.determine_price(prices)
        all_items.append(item)

    return all_items


if __name__ == "__main__":
    prices = retrieve_prices()
    type_mapper = type_mapping(prices)
    items = build_items(prices, type_mapper)
