
import pytest
import pendulum
from poe.valuation.framework.models import ItemQuery
from poe.valuation.framework.valuation import Valuation
from poe.valuation.framework.price_store import HashKeyPriceStore
from poe.valuation.framework.manifester import Manifester
from poe.valuation.framework.new_rules import the_artist

def test_the_artist_valuation():
    # Mock Data based on live values
    # The Artist: 30c
    # Enhance Support Lvl 4 Corrupted: 608.7c
    
    artist_query = ItemQuery(name="The Artist")
    enhance_query = ItemQuery(name="Enhance Support", gemLevel=4, corrupted=True)
    
    valuations = [
        Valuation(
            key=artist_query,
            estimate=30.0,
            timestamp=pendulum.now().int_timestamp,
            tags=["DivinationCard"],
            info="The Artist"
        ),
        Valuation(
            key=enhance_query,
            estimate=608.7,
            timestamp=pendulum.now().int_timestamp,
            tags=["SkillGem"],
            info="Enhance Support"
        )
    ]
    
    price_store = HashKeyPriceStore(valuations)
    manifester = Manifester(price_store)
    
    rule = the_artist()
    outcome = manifester.manifest(rule)
    
    # Expected Calculation:
    # Cost = 11 * 30 = 330
    # Revenue = 608.7
    # Profit (Total) = 608.7 - 330 = 278.7
    # Multiplier = 1/11
    # Profit (Per Card) = 278.7 / 11 = 25.33636...
    # Estimate (Per Card) = 30 + 25.33636... = 55.33636...
    
    assert outcome.info.startswith("The Artist")
    
    # Parse info string "The Artist | Profit: 25.34 | Risk: 0.00"
    parts = outcome.info.split("|")
    profit_str = parts[1].split(":")[1].strip()
    profit = float(profit_str)
    
    assert abs(profit - 25.34) < 0.01
    assert abs(outcome.estimate - 55.34) < 0.01
    
    print(f"Test Passed! Profit: {profit}, Estimate: {outcome.estimate}")

if __name__ == "__main__":
    test_the_artist_valuation()
