from dataclasses import dataclass
from typing import Mapping

from poe.constants import blacklist
from poe.item.item_factory import item_factory
from poe.ninja import retrieve_prices
from poe.trade.stash_tabs.all_tabs_getter import get_all_tabs
from poe.item.type_determiner import type_mapping
from poe.valuation import own_valuations


@dataclass
class ItemBuilder:
    prices: dict
    values: Mapping

    def build_items(self, items):
        type_mapper = type_mapping(self.prices)
        types = map(type_mapper, items)
        items = [
            {"type": t, **item}
            for item, t in zip(items, types)
            if not item["typeLine"] in blacklist
        ]
        all_items = []
        for old_item in items:
            if not old_item["type"]:
                print(f"Could not find an item type for {old_item['typeLine']}")
                continue
            # if old_item["type"] in {"Base"}:
            #     continue
            if old_item["type"] in {
                "Heist",
                "Expedition",
                "Watchstone",
                "Organ",
                "CurrencyShard",
                "Flask",
            }:
                continue
            item = item_factory(**old_item)
            item.determine_price(self.prices, self.values)
            all_items.append(item)

        return all_items


if __name__ == "__main__":
    prices = retrieve_prices()
    valuations = own_valuations(prices)
    type_mapper = type_mapping(prices)
    item_builder = ItemBuilder(prices, valuations)
    items = item_builder.build_items(get_all_tabs(25))
