from constants import TRANSMUTE
from poe.ninja import retrieve_prices
from poe.valuation.framework.ninja_adapter import NinjaAdapter
from valuation.framework.new_rules import vaal_exceptional, level_exceptional, portal_scroll
from valuation.framework.manifester import Manifester
from valuation.framework.price_store import HashKeyPriceStore
from valuation.framework.profit import profitability_analysis


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
