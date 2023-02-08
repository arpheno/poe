from poe.constants import TRANSMUTE
from poe.ninja import retrieve_prices
from poe.valuation.framework.ninja_adapter import NinjaAdapter
from poe.valuation.framework.new_rules import vaal_exceptional, level_exceptional, portal_scroll, the_enlightened
from poe.valuation.framework.manifester import Manifester
from poe.valuation.framework.price_store import HashKeyPriceStore
from poe.valuation.framework.profit import profitability_analysis

from poe.valuation.framework.tft_adapter import TftAdapter


def test_adapt_ninja():
    prices = retrieve_prices()
    adapter = NinjaAdapter()
    tft_adapter = TftAdapter()
    tft_valuations = tft_adapter.adapt()
    valuations = adapter.adapt(prices)
    price_store = HashKeyPriceStore(valuations)
    price_store.add(tft_valuations)

    rules = (
            level_exceptional()
            + vaal_exceptional()
            + [portal_scroll(),the_enlightened()]
    )
    manifester = Manifester(price_store)
    price_store.add([manifester.manifest(rule) for rule in rules])
    profitable_items = [profitability_analysis(valuations) for valuations in price_store.values() if
                        len(valuations) > 1]
    transmute = price_store.query({'name': TRANSMUTE})
    assert rules
