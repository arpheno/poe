from typing import List

from poe.item.map import Map


def match_map(candidates: List[dict], item: Map):
    conditions = [
        lambda x: x["mapTier"] == item.map_tier,
    ]
    for candidate in candidates:
        if all(f(candidate) for f in conditions):
            return candidate
    print(f"Couldn't find match for {item.name} {item.map_tier}", end=" ")
    approximate_match = candidates[-1]
    print(f"Using {item.name}, " f"{approximate_match['mapTier']} ")
    return approximate_match
