from poe.timeless.query import query_timeless_jewel
from poe.trade.query_resolver import resolve_query


def find_doryiani(seed: int, name_of="timeless"):

    data = query_timeless_jewel(name_of, seed)
    result_hash = resolve_query(data)
    return result_hash


