from functools import partial


from poe.splinters.domain.splinter_info import SplinterInfo
from poe.splinters.splinter_profiter import splinter_profitability
from poe.splinters.trades_resolver import resolve_to_trades


def find_profit_in_splinters(splinter_info: SplinterInfo):
    splinters = splinter_profitability(
        splinter_info.completed_set_price, splinter_info.set_size, splinter_info.splinter_price
    )
    df = (
        splinters.reset_index()
        .groupby("index")
        .apply(partial(resolve_to_trades, splinter_query=splinter_info.splinter_query))
    )
    return df
