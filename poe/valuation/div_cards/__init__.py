import inspect

from constants import blacklist
from poe.valuation.div_cards import rules
from poe.valuation.div_cards.generic import expand_currency_shards
from poe.valuation.div_cards.rules import xxxmap_div_card_name, div_card_rules
from poe.ninja import retrieve_prices



def div_card_values(prices):
    rule_based = {name: func(prices) for name, func in div_card_rules.items()}
    generic = {key: value for key, value in expand_currency_shards(prices).items()}
    blacklisted = {key: 0 for key in blacklist}
    return {**rule_based, **generic, **blacklisted}


if __name__ == "__main__":
    prices = retrieve_prices()
    div_card_values(prices)
