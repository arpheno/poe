import sys

sys.path.append("/home/dhokuav/poe")

from poe.ninja import retrieve_prices
from poe.valuation.div_cards.fixed import currency_shards

import logging

logger = logging.getLogger(__name__)


def apply_fixed_rules(prices):
    result = {}
    for splinter, (fraction, reward) in currency_shards.items():
        try:
            reward_price = min(
                [price for price in prices.get(reward, [{}])],
                key=lambda x: x.get("links", 0),
            )
            if reward_price and reward_price.get("sparkLine"):
                result[splinter] = fraction * reward_price["chaosValue"]
            else:
                result[splinter] = 0
        except ValueError:
            pass
        except Exception:
            logger.exception(f"Can't value {splinter}")
    return result


if __name__ == "__main__":
    prices = retrieve_prices()
    result = apply_fixed_rules(prices)
    # for key, value in result.items():
    #     reward_price = min(
    #         [price for price in prices.get(key, [{}])], key=lambda x: x.get("links", 0)
    #     )
    #     if reward_price:
    #         print(
    #             f'{key} ninja {reward_price["chaosValue"]} own {value} diff {reward_price["chaosValue"]-value}'
    #         )
    print(result)
