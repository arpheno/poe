import json
from constants import blacklist
from poe.ninja import retrieve_prices
from poe.valuation.div_cards import rules
from poe.valuation.div_cards.generic import apply_fixed_rules
from poe.valuation.div_cards.rules import xxxmap_div_card_name, div_card_rules
import logging

logger = logging.getLogger(__name__)


def div_card_values(prices):
    rule_based = {}
    for name, func in div_card_rules.items():
        try:
            rule_based[name] = func(prices)
        except ValueError:
            pass
        except Exception:
            logger.exception(f"Can't value {name}")

    generic = {key: value for key, value in apply_fixed_rules(prices).items()}
    blacklisted = {key: 0 for key in blacklist}
    return {**rule_based, **generic, **blacklisted}


if __name__ == "__main__":
    prices = retrieve_prices()
    # with open("prices.json", "r") as f:
    #     prices = json.load(f)
    div_card_values(prices)
