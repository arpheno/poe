from collections import defaultdict

from poe.constants import TRANSMUTE
from poe.ninja import retrieve_prices
from poe.valuation.framework.ninja_adapter import NinjaAdapter
from poe.valuation.framework.new_rules import vaal_exceptional, level_exceptional, portal_scroll, the_enlightened, \
    gemcutters_mercy
from poe.valuation.framework.manifester import Manifester
from poe.valuation.framework.price_store import HashKeyPriceStore
from poe.valuation.framework.profit import profitability_analysis
from poe.valuation.framework.tft_adapter.adapter import TftAdapter
from poe.valuation.framework.valuation import Valuation


def test_adapt_ninja():
    prices = retrieve_prices()
    adapter = NinjaAdapter()
    tft_adapter = TftAdapter()
    tft_valuations = tft_adapter.adapt()
    valuations = adapter.adapt(prices)
    price_store = HashKeyPriceStore(valuations)
    price_store.add(tft_valuations)

    flat_prices = [
        # {"name": "doryani institute (gem)", "chaosvalue": 125},
        Valuation(key=dict(name='5way'), estimate=400 / 37, timestamp=0, tags=['tft']),
        # {"hash_key": "5way", "chaosvalue": 400 / 39},
        #    {"hash_key": "5waygcp", "chaosvalue": 400 / 78},
    ]
    price_store.add(flat_prices)
    rules = (
            level_exceptional()
            + vaal_exceptional()
            + [gemcutters_mercy()]
    )
    manifester = Manifester(price_store)
    price_store.add([manifester.manifest(rule) for rule in rules])
    profitable_items = [profitability_analysis(valuations) for valuations in price_store.values() if
                        len(valuations) > 1]
    transmute = price_store.query({'name': TRANSMUTE})
    truly_profitable = [p for l in profitable_items for p in l if p.absolute_profit > 0]
    [mercy] = [p for p in truly_profitable if p.valuation.key['name'] == "Gemcutter's Mercy"]
    activities=defaultdict(dict)
    [enhance] = [p for p in truly_profitable if p.valuation.key['name'] == "Enhance Support" if
                 p.valuation.info == 'Regular leveling']
    [empower] = [p for p in truly_profitable if p.valuation.key['name'] == "Empower Support" if
                 p.valuation.info == 'Regular leveling']
    [enlighten] = [p for p in truly_profitable if p.valuation.key['name'] == "Enlighten Support" if
                   p.valuation.info == 'Regular leveling']
    total_profit_per_card = (sum(
        g.absolute_profit for g in [enhance, empower, enlighten]) / 3 + 3 * mercy.absolute_profit) / 3
    assert rules
