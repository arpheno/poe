import pandas as pd

from poe.ninja import retrieve_prices
from poe.valuation.splinters.domain.breach import breach_splinters
from poe.valuation.splinters.domain.simulacrum import simulacrum_splinters
from poe.valuation.splinters.domain.timeless import timeless_splinters

import logging

logger = logging.getLogger(__name__)


def splinter_values(prices):
    values = []
    for f in [
        breach_splinters,
        timeless_splinters,
        simulacrum_splinters,
    ]:
        try:
            values.append(f(prices))
        except ValueError:
            pass
        except Exception:
            logger.exception(f"Can't value {f.__name__}")
    df = pd.concat(values)
    return df.to_dict()


if __name__ == "__main__":
    prices = retrieve_prices(["Fragment", "Currency"])
    result = splinter_values(prices)
    print(result)
