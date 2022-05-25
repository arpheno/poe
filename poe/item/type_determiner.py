from typing import Callable

from constants import HARD_CURRENCY


def type_mapping(prices) -> Callable:
    all_rates = {key: values for m in prices.maps for key, values in m.items()}
    mapping = {name: first["type"] for name, (first, *_) in all_rates.items()}
    type_mapper = determine_type(mapping)
    return type_mapper


def determine_type(type_mapping) -> Callable:
    return (
        lambda item: is_hard_currency(item, type_mapping)
        or is_item_exact_match(item, type_mapping)
        or is_item_influenced(item, type_mapping)
        or is_heist(item, type_mapping)
        or is_expedition(item, type_mapping)
        or is_organ(item, type_mapping)
        or is_cluster_jewel(item, type_mapping)
        or is_currency_shard(item, type_mapping)
        or is_flask(item, type_mapping)
    )


def is_hard_currency(item, type_mapping):
    return "Hard Currency" if item["typeLine"] in HARD_CURRENCY else None


def is_item_exact_match(item, type_mapping):
    return type_mapping.get(item["typeLine"]) or type_mapping.get(
        item["typeLine"] + " Support"
    )


def is_item_influenced(item, type_mapping):
    return "Base" if item.get("influences") else None


def is_heist(item, type_mapping):
    return (
        "Heist"
        if (
            "ontract:" in item["typeLine"]
            or "lueprint:" in item["typeLine"]
            or ("Heist" in item["stashtab"])
        )
        else None
    )


def is_expedition(item, type_mapping):
    return "Expedition" if ("Expedition" in item["stashtab"]) else None


def is_watchstone(item, type_mapping):
    return "Watchstone" if ("Watchstone" in item["typeLine"]) else None


def is_organ(item, type_mapping):
    return "Organ" if "Tane's Laboratory" in item.get("descrText", "") else None


def is_currency_shard(item, type_mapping):
    return (
        "CurrencyShard"
        if item["typeLine"].endswith("Shard") or item["typeLine"].endswith("Scrap")
        else None
    )


def is_cluster_jewel(item, type_mapping):
    return "ClusterJewel" if "Cluster Jewel" in item["baseType"] else None


def is_flask(item, type_mapping):
    return "Flask" if "Flask" in item["typeLine"] else None
