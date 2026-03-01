
import sys
import os
sys.path.append(os.getcwd())

from poe.ninja import retrieve_prices
from poe.trade.prices import get_doryani_institute_price
from poe.valuation.framework.models import ItemQuery, Ingredient
from poe.valuation.framework.transformationrule import TransformationRule
from poe.valuation.framework.valuation import Valuation
from poe.valuation.framework.price_store import HashKeyPriceStore
from poe.valuation.framework.manifester import Manifester
import pendulum
import numpy as np

def debug_enlighten_double_corrupt():
    print("Fetching prices...")
    prices = retrieve_prices(["SkillGem", "DivinationCard", "Currency"])
    doryani_price = get_doryani_institute_price()
    print(f"Doryani's Institute Price: {doryani_price}c")

    valuations = []
    for category, items in prices.items():
        for item in items:
            query = ItemQuery(
                name=item.get('name'),
                gemLevel=item.get('gemLevel'),
                gemQuality=item.get('gemQuality'),
                corrupted=item.get('corrupted', False),
            )
            val = Valuation(
                key=query,
                estimate=item.get('chaosValue', 0),
                timestamp=pendulum.now().int_timestamp,
                tags=[category],
                info=item.get('name')
            )
            valuations.append(val)
    
    valuations.append(Valuation(key=ItemQuery(name="Doryani's Institute"), estimate=doryani_price, timestamp=0, tags=['custom'], info="Doryani's Institute"))

    price_store = HashKeyPriceStore(valuations)
    manifester = Manifester(price_store)

    # Define the rule manually to match new_rules.py
    item_name = "Enlighten Support"
    ingredients = [
        Ingredient(query=ItemQuery(name=item_name, gemLevel=3, corrupted=False), quantity=1),
        Ingredient(query=ItemQuery(name="Doryani's Institute"), quantity=1)
    ]
    products = [
        ItemQuery(name=item_name, gemLevel=4, corrupted=True),
        ItemQuery(name=item_name, gemLevel=3, corrupted=True),
        ItemQuery(name=item_name, gemLevel=2, corrupted=True),
    ]
    probabilities = [0.25, 0.5, 0.25]
    
    rule = TransformationRule(
        ingredients=ingredients, 
        products=products, 
        probabilities=probabilities, 
        info=f"Temple Vaal {item_name}",
        tags=['scheme', 'vaaling']
    )

    print("\n--- Ingredients ---")
    total_cost = 0
    for ing in ingredients:
        candidates = price_store.query(ing.query)
        if not candidates:
            print(f"Missing price for {ing.query}")
            # Debug: print all Enlighten valuations
            if "Enlighten" in ing.query.name:
                print("Available Enlighten valuations:")
                for v in valuations:
                    if "Enlighten" in v.key.name:
                        print(f"  - Name: {v.key.name}, Lvl: {v.key.gem_level}, Qual: {v.key.gem_quality}, Corr: {v.key.corrupted}, Estimate: {v.estimate}c")
                        print(f"    Hash Key: {v.hash_key}")
            continue
        best = min(candidates, key=lambda x: x.estimate)
        cost = best.estimate * ing.quantity
        total_cost += cost
        print(f"{ing.query.name} (Lvl {ing.query.gem_level}, Qual {ing.query.gem_quality}, Corr {ing.query.corrupted}): {best.estimate}c")
    
    print(f"Total Cost: {total_cost}c")

    print("\n--- Products ---")
    expected_revenue = 0
    for i, prod in enumerate(products):
        candidates = price_store.query(prod)
        if not candidates:
            print(f"Missing price for {prod}")
            continue
        best = min(candidates, key=lambda x: x.estimate)
        revenue = best.estimate * probabilities[i]
        expected_revenue += revenue
        print(f"{prod.name} (Lvl {prod.gem_level}, Corr {prod.corrupted}): {best.estimate}c (Prob: {probabilities[i]}) -> Exp: {revenue}c")

    print(f"Total Expected Revenue: {expected_revenue}c")
    print(f"Profit: {expected_revenue - total_cost}c")

    # Run manifester
    outcome = manifester.manifest(rule)
    print(f"\nManifester Outcome: {outcome.info}")
    if outcome.breakdown:
        print(f"Breakdown Profit: {outcome.breakdown['profit']}")
        print(f"Breakdown Scaled Profit: {outcome.breakdown['scaled_profit']}")

if __name__ == "__main__":
    debug_enlighten_double_corrupt()
