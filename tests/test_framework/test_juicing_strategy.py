from poe.ninja import retrieve_prices
from poe.valuation.framework.ninja_adapter import NinjaAdapter
from poe.valuation.framework.price_store import HashKeyPriceStore
from poe.valuation.framework.tft_adapter.adapter import TftAdapter


def test_cemetery_cost_per_map():
    prices = retrieve_prices()
    adapter = NinjaAdapter()
    tft_adapter = TftAdapter()
    tft_valuations = tft_adapter.adapt()
    valuations = adapter.adapt(prices)
    price_store = HashKeyPriceStore(valuations)
    price_store.add(tft_valuations)
    ingredients=[
        'Gilded Divination Scarab',
        'Gilded Ambush Scarab',
        'Gilded Reliquary Scarab',
        'Polished Legion Scarab',
        'Mirror of Delirium',
        '3 Strongboxes Corrupted',
        'Legion',
        'Strongbox Enraged',
        ]
    costs={
        key:price_store.query({'name':key})[0].estimate for key in ingredients
    }
    costs['Mirror of Delirium']/=4
    costs['Legion']/=4
    costs['Strongbox Enraged']/=4
    costs['3 Strongboxes Corrupted']/=16
    total=sum(value for value in costs.values())
    print(costs)
