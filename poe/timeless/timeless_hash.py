from poe.trade.query_resolver import trade_resolver

from poe.timeless.query import query_timeless_jewel


def find_doryiani(seed: int, name_of="timeless"):

    data = query_timeless_jewel(name_of, seed)
    result_hash, _ = trade_resolver(data)
    return result_hash
