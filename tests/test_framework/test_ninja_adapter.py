from dataclasses import dataclass

from constants import PORTAL, TRANSMUTE
from poe.ninja import retrieve_prices
from poe.valuation.framework.ninja_adapter import NinjaAdapter
from valuation.div_cards.new_rules import vaal_exceptional, level_exceptional
from valuation.framework.manifester import Manifester
from valuation.framework.price_store import HashKeyPriceStore
from valuation.framework.rule import Rule
from valuation.framework.valuation import Valuation


def portal_scroll():
    return Rule(
        [dict(name=TRANSMUTE)],
        [dict(name=PORTAL)],
        probabilities=[1],
        info="Convert Transmutes to Portals",
        multiplier=4 / 3,
    )


@dataclass
class Profitability:
    valuation: Valuation
    absolute_profit: float
    relative_profit: float


def profitability_analysis(valuations: [Valuation]):
    lowest_purchasable = min(valuation.estimate for valuation in valuations if 'purchasable' in valuation.tags)
    return [Profitability(valuation,absolute_profit=valuation.estimate-lowest_purchasable,relative_profit=(valuation.estimate-lowest_purchasable)/lowest_purchasable) for valuation in valuations]


def test_adapt_ninja():
    prices = retrieve_prices()
    adapter = NinjaAdapter()
    valuations = adapter.adapt(prices)
    price_store = HashKeyPriceStore(valuations)

    rules = (
            level_exceptional()
            + vaal_exceptional()
            + [portal_scroll()]
    )
    manifester = Manifester(price_store)
    price_store.add([manifester.manifest(rule) for rule in rules])
    profitable_items = [profitability_analysis(valuations) for valuations in price_store.values() if len(valuations) > 1]
    transmute = price_store.query({'name': TRANSMUTE})
    assert rules
