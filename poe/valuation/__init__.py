from poe.ninja import retrieve_prices
from poe.valuation.currency import currency_valuation
from poe.valuation.div_cards import div_card_values
from poe.valuation.scarabs.main import scarab_orb_of_horizon
from poe.valuation.splinters import splinter_values


def own_valuations(prices):
    scarabs = scarab_orb_of_horizon(prices)
    scarabs = scarabs[["price", "value"]].max(axis=1).reset_index()
    scarabs["name"] = scarabs.tier + " " + scarabs.kind + " Scarab"
    scarabs = scarabs[["name", 0]].set_index("name")[0].to_dict()
    div_cards = div_card_values(prices)
    splinters = splinter_values(prices)
    currency = currency_valuation(prices)
    values = {**scarabs, **div_cards, **splinters,**currency}
    return values


if __name__ == "__main__":
    prices = retrieve_prices()
    own_valuations(prices)
