from poe.ninja import retrieve_prices
from poe.valuation.div_cards.new_rules import terrible_secret_of_space, gemcutters_mercy, temple_vaal_enlighten
from poe.valuation.framework.manifester import Manifester
from poe.valuation.framework.price_store import FlatPriceStore


def test_manifester_maps_items_correctly():
    flat_prices = [{'type': "SkillGem",
                    'gemLevel': level,
                    'gemQuality': 20,
                    'sparkLine': {'data': 1}
                    } for level in (20, 21)]  # retrieve_prices(['SkillGem'], league='Standard')
    flat_price_store = FlatPriceStore(flat_prices)
    manifester = Manifester(flat_price_store)

    def func(item):
        return item["type"] == "SkillGem" and \
               item["gemLevel"] == 21 and \
               item.get("gemQuality") == 23 and \
               item.get('name') == 'Vaal Molten Shell' and \
               item["sparkline"]["data"]

    result = manifester.map_to_concrete_items(func)
    assert result


def test_manifest_terrible_secret_of_space():
    prices = retrieve_prices(['SkillGem', 'DivinationCard'])
    flat_prices = [p for l in prices.values() for p in l]
    price_store = FlatPriceStore(flat_prices)
    manifester = Manifester(price_store)
    outcome = manifester.manifest(terrible_secret_of_space())
    print(outcome.mean, outcome.stdev)


def test_manifest_gemcutters_mercy():
    prices = retrieve_prices(['SkillGem', 'DivinationCard'])
    flat_prices = [p for l in prices.values() for p in l]
    price_store = FlatPriceStore(flat_prices)
    manifester = Manifester(price_store)
    outcome = manifester.manifest(gemcutters_mercy())
    print(outcome.mean, outcome.stdev)


def test_manifest_temple_vaal_enlighten():
    prices = retrieve_prices(['SkillGem', 'DivinationCard'])
    flat_prices = [p for l in prices.values() for p in l] + [{'name': "Doryani's Institue", "chaosValue": 125}]
    price_store = FlatPriceStore(flat_prices)
    manifester = Manifester(price_store)
    outcome = manifester.manifest(temple_vaal_enlighten())
    print(outcome.mean, outcome.stdev)
