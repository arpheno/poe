from pprint import pprint

from poe.constants import TRANSMUTE, PORTAL
from poe.ninja import retrieve_prices
from poe.valuation.framework.manifester import Manifester
from poe.valuation.framework.price_store import FlatPriceStore, HashKeyPriceStore
from poe.valuation.framework.transformationrule import TransformationRule


def terrible_secret_of_space():
    products = [
        lambda item: "Golem" in item["name"]
                     and item["type"] == "SkillGem"
                     and item["gemLevel"] == 21
                     and item.get("gemQuality") == 23
                     and item["sparkline"]["data"]
    ]
    ingredients = [lambda item: item["name"] == "Terrible Secret of Space"] * 8
    return TransformationRule(
        ingredients,
        products,
        probabilities=[1 / 18] * 18,
        multiplier=1 / 8,
    )

def the_enlightened():
    ingredients = [
        dict(name='The Enlightened')
    ] * 6
    products = (
        {"name": 'Enlighten Support', 'gem_level': 3, 'corrupted': None, 'gem_quality': None},
    )
    probabilities = (1,)
    return TransformationRule(ingredients, products, probabilities, info="The Enlightened",
                              tags=['divination_card', 'combining', 'gamble']
                              )

def home():
    products=[
        dict(name=item_name, gem_level=1, gem_quality=None, corrupted=None )
        for item_name in ("Enlighten Support", "Empower Support", "Enhance Support")
    ]
    ingredients =[dict(name="Home")] * 3
    return TransformationRule(
        ingredients,
        products,
        probabilities=[1 / 3] * 3,
        multiplier=1 / 3,
        tags=['divination_card', 'combining', 'gamble']
    )
def gemcutters_mercy():
    products=[
        dict(name=item_name, gem_level=1, gem_quality=None, corrupted=None )
        for item_name in ("Enlighten Support", "Empower Support", "Enhance Support")
    ]
    ingredients =[dict(name="Gemcutter's Mercy")] * 3
    return TransformationRule(
        ingredients,
        products,
        probabilities=[1 / 3] * 3,
        multiplier=1 / 3,
        tags=['divination_card', 'combining', 'gamble']
    )


def temple_vaal_one_exceptional(item_name):
    ingredients = (
        dict(name=item_name, gem_level=3, gem_quality=None, corrupted=None, ),
        dict(name="Doryani Institute (Gem)")
    )
    products = (
        {"name": item_name, 'gem_level': 4, 'corrupted': True, 'gem_quality': None},
        {"name": item_name, 'gem_level': 3, 'corrupted': True, 'gem_quality': None},
        {"name": item_name, 'gem_level': 2, 'corrupted': True, 'gem_quality': None},
    )
    probabilities = (1 / 4, 2 / 4, 1 / 4)
    return TransformationRule(ingredients, products, probabilities, info="Temple Vaal",
                              tags=['scheme', 'vaaling']
                              )


def vaal_one_exceptional(item_name):
    ingredients = (
        dict(name=item_name, gem_level=3, gem_quality=None, corrupted=None, ),
        dict(name='Vaal Orb')
    )
    products = (
        {"name": item_name, 'gem_level': 4, 'corrupted': True, 'gem_quality': None},
        {"name": item_name, 'gem_level': 3, 'corrupted': True, 'gem_quality': None},
        {"name": item_name, 'gem_level': 2, 'corrupted': True, 'gem_quality': None},
    )
    probabilities = (1 / 8, 6 / 8, 1 / 8)
    return TransformationRule(ingredients, products, probabilities, info="Regular Vaal",
                              tags=['scheme', 'vaaling']
                              )


def vaal_exceptional():
    temple = [
        temple_vaal_one_exceptional(f"{gem} Support")
        for gem in ["Enlighten", "Empower", "Enhance"]
    ]
    regular = [
        vaal_one_exceptional(f"{gem} Support")
        for gem in ["Enlighten", "Empower", "Enhance"]
    ]
    return temple + regular


def gcp_level_exceptional(item_name):
    ingredients = [
                      dict(name=item_name, gem_level=1, gem_quality=None, corrupted=None, ),
                      dict(name="5waygcp")
                  ] + [dict(name="Gemcutter's Prism")] * 20
    products = [
        dict(name=item_name, gem_level=3, gem_quality=None, corrupted=None, ),
    ]
    probabilities = [1]
    return TransformationRule(
        ingredients,
        products,
        probabilities,
        info="GCP leveling",
        tags=['scheme', 'leveling']
    )


def regular_level_exceptional(item_name):
    ingredients = [
        dict(name=item_name, gem_level=1, gem_quality=None, corrupted=None, ),
        dict(name="5way")
    ]
    products = [
        dict(name=item_name, gem_level=3, gem_quality=None, corrupted=None, ),
    ]
    probabilities = [1]
    return TransformationRule(
        ingredients, products, probabilities, info="Regular leveling"
    )


def level_exceptional():
    gcp = [
        gcp_level_exceptional(f"{gem} Support")
        for gem in ["Enlighten", "Empower", "Enhance"]
    ]
    regular = [
        regular_level_exceptional(f"{gem} Support")
        for gem in ["Enlighten", "Empower", "Enhance"]
    ]
    return gcp + regular


def portal_scroll():
    return TransformationRule(
        [dict(name=TRANSMUTE)],
        [dict(name=PORTAL)],
        probabilities=[1],
        info="Convert Transmutes topi Portals",
        multiplier=4 / 3,
    )
def the_dragons_heart():
    ingredients = (
        dict(name='The Dragon\'s Heart'),
    ) * 11
    products = (
        {"name": "Empower Support", 'gem_level': 4, 'corrupted': True, 'gem_quality': None},
    )
    probabilities = (1,)
    return TransformationRule(ingredients, products, probabilities, multiplier=1/11, info="The Dragon's Heart",
                              tags=['divination_card', 'empower']
                              )
def the_artist():
    ingredients = (
        dict(name='The Artist'),
    ) * 11
    products = (
        {"name": "Enhance Support", 'gem_level': 4, 'corrupted': False, 'gem_quality': None},
    )
    probabilities = (1,)
    return TransformationRule(ingredients, products, probabilities, multiplier=1/11, info="The Artist",
                              tags=['divination_card', 'enhance']
                              )
def wealth_and_power():
    ingredients = (
        dict(name='Wealth and Power'),
    ) * 11
    products = (
        {"name": "Enlighten Support", 'gem_level': 4, 'corrupted': True, 'gem_quality': None},
    )
    probabilities = (1,)
    return TransformationRule(ingredients, products, probabilities, multiplier=1/11, info="Wealth and Power",
                              tags=['divination_card', 'enlighten']
                              )


if __name__ == "__main__":
    prices = retrieve_prices(["SkillGem", "DivinationCard", "Currency"])
    flat_prices = [p for l in prices.values() for p in l] + [
        # {"name": "doryani institute (gem)", "chaosvalue": 125},
        {"name": "5way", "chaosvalue": 400 / 39},
        {"name": "5waygcp", "chaosvalue": 400 / 78},
    ]
    price_store = HashKeyPriceStore(flat_prices)
    manifester = Manifester(price_store)
    rules = (
            level_exceptional()
            + vaal_exceptional()
            + [terrible_secret_of_space(), gemcutters_mercy(), portal_scroll()]
    )
    outcomes = [manifester.manifest(rule) for rule in rules]
    pprint(outcomes)
