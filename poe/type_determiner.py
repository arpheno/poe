import operator
from functools import reduce
from typing import Callable


def type_mapping(prices) -> Callable:
    all_rates = {key: values for m in prices.maps for key, values in m.items()}
    mapping = {name: first["type"] for name, (first, *_) in all_rates.items()}
    type_mapper = determine_type(mapping)
    return type_mapper


def determine_type(type_mapping) -> Callable:
    return lambda item: is_item_exact_match(item, type_mapping) or is_item_influenced(item, type_mapping)


def is_chaos_orb(item, type_mapping):
    return "Currency" if item["typeLine"] == "Chaos Orb" else None


def is_item_exact_match(item, type_mapping):
    return type_mapping.get(item["typeLine"]) or type_mapping.get(item["typeLine"] + " Support")


def is_item_influenced(item, type_mapping):
    return "Base" if item.get("influences") else None
