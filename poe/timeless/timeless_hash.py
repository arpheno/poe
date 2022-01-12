from poe.timeless.query import query_timeless_jewel
from poe.trade.query_resolver import trade_resolver


def find_doryiani(seed: int, name_of="timeless"):

    data = query_timeless_jewel(name_of, seed)
    result_hash,_ = trade_resolver(data)
    return result_hash


