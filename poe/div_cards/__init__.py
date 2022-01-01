import inspect

from Levenshtein.StringMatcher import StringMatcher

from constants import blacklist
from poe.div_cards import rules
from poe.div_cards.generic import expand_currency_shards
from poe.div_cards.rules import xxxmap_div_card_name
from poe.ninja import retrieve_prices

functions_list = inspect.getmembers(rules, inspect.isfunction)


def div_card_values():
    prices = retrieve_prices( )
    rule_based={name:func(prices) for name, func in functions_list[:-2]}
    generic={xxxmap_div_card_name(key):value for key,value in expand_currency_shards(prices).items()}
    for div_card_name, value in rule_based.items():
        print(f"{div_card_name}:{value}")
    blacklisted={xxxmap_div_card_name(key):0 for key in blacklist}
    return {**rule_based,**generic,**blacklisted}
if __name__ == "__main__":
    div_card_values()
