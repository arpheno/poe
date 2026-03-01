from pprint import pprint
from typing import List

from poe.constants import TRANSMUTE, PORTAL
from poe.valuation.framework.models import Ingredient, ItemQuery
from poe.valuation.framework.transformationrule import TransformationRule
from poe.valuation.framework.manifester import Manifester
from poe.valuation.framework.price_store import HashKeyPriceStore
from poe.ninja import retrieve_prices

def terrible_secret_of_space():
    # 8x Terrible Secret of Space -> 1x Golem Gem (Lvl 21, Qual 23)
    golems = [
        "Summon Ice Golem of Shattering",
        "Summon Lightning Golem of Hordes",
        "Summon Flame Golem of Hordes",
        "Summon Stone Golem of Hordes",
        "Summon Carrion Golem of Scavenging",
        "Summon Carrion Golem of Hordes",
        "Summon Flame Golem of the Meteor",
        "Summon Chaos Golem of the Maelström",
        "Summon Ice Golem of Hordes",
        "Summon Chaos Golem of Hordes",
        "Summon Stone Golem of Safeguarding"
    ]
    
    products = [
        ItemQuery(name=name, gemLevel=21, gemQuality=23, corrupted=True)
        for name in golems
    ]
    
    ingredients = [Ingredient(query=ItemQuery(name="Terrible Secret of Space"), quantity=8)]
    
    return TransformationRule(
        ingredients=ingredients,
        products=products,
        probabilities=[1/len(products)] * len(products),
        multiplier=1/8, # Profit per card
        info="Terrible Secret of Space",
        tags=['divination_card', 'golem']
    )

def the_enlightened():
    ingredients = [Ingredient(query=ItemQuery(name='The Enlightened'), quantity=6)]
    products = [
        ItemQuery(name='Enlighten Support', gemLevel=3, corrupted=False)
    ]
    probabilities = [1.0]
    return TransformationRule(
        ingredients=ingredients, 
        products=products, 
        probabilities=probabilities, 
        multiplier=1/6,
        info="The Enlightened",
        tags=['divination_card', 'combining', 'gamble']
    )

def home():
    products=[
        ItemQuery(name=item_name, gemLevel=1, gemQuality=0, corrupted=False)
        for item_name in ("Enlighten Support", "Empower Support", "Enhance Support")
    ]
    ingredients = [Ingredient(query=ItemQuery(name="Home"), quantity=3)]
    return TransformationRule(
        ingredients=ingredients,
        products=products,
        probabilities=[1 / 3] * 3,
        multiplier=1 / 3,
        tags=['divination_card', 'combining', 'gamble'],
        info="Home"
    )

def gemcutters_mercy():
    products=[
        ItemQuery(name=item_name, gemLevel=1, gemQuality=0, corrupted=False)
        for item_name in ("Enlighten Support", "Empower Support", "Enhance Support")
    ]
    ingredients = [Ingredient(query=ItemQuery(name="Gemcutter's Mercy"), quantity=3)]
    return TransformationRule(
        ingredients=ingredients,
        products=products,
        probabilities=[1 / 3] * 3,
        multiplier=1 / 3,
        tags=['divination_card', 'combining', 'gamble'],
        info="Gemcutter's Mercy"
    )


def temple_vaal_one_exceptional(item_name):
    ingredients = [
        Ingredient(query=ItemQuery(name=item_name, gemLevel=3, corrupted=False), quantity=1),
        Ingredient(query=ItemQuery(name="Doryani's Institute"), quantity=1) # Assuming this is the item name for the temple room or vessel?
        # Actually, Doryani's Institute is a room. If we buy it, we buy a Chronicle of Atzoatl?
        # Or maybe we just value the room itself?
        # The original code had "Doryani Institute (Gem)".
        # Let's assume we buy a temple with the room.
    ]
    products = [
        ItemQuery(name=item_name, gemLevel=4, corrupted=True),
        ItemQuery(name=item_name, gemLevel=3, corrupted=True),
        ItemQuery(name=item_name, gemLevel=2, corrupted=True), # Poof? Or just corrupted?
        # Temple double corrupt:
        # 1. +1 Level / +1 Level (Not possible on gems, max is +1)
        # Gems:
        # 25% +1 Level (Max 4)
        # 25% -1 Level (Min 2)
        # 25% +Quality (Max 23)
        # 25% -Quality
        # Wait, Temple on Gems allows Level 21/23.
        # But for Exceptional gems (Max 3), +1 makes it 4.
        # Temple can do:
        # - Add Vaal skill (not for exceptional)
        # - Change to Vaal version (not for exceptional)
        # - Add quality
        # - Remove quality
        # - Add level
        # - Remove level
        # It applies TWO corruptions.
        
        # For simplicity, let's stick to the original probabilities if they were correct.
        # Original: 1/4 Lvl 4, 2/4 Lvl 3, 1/4 Lvl 2.
    ]
    probabilities = [0.25, 0.5, 0.25]
    return TransformationRule(
        ingredients=ingredients, 
        products=products, 
        probabilities=probabilities, 
        info=f"Temple Vaal {item_name}",
        tags=['scheme', 'vaaling']
    )


def vaal_one_exceptional(item_name):
    ingredients = [
        Ingredient(query=ItemQuery(name=item_name, gemLevel=3, corrupted=False), quantity=1),
        Ingredient(query=ItemQuery(name='Vaal Orb'), quantity=1)
    ]
    products = [
        ItemQuery(name=item_name, gemLevel=4, corrupted=True),
        ItemQuery(name=item_name, gemLevel=3, corrupted=True),
        ItemQuery(name=item_name, gemLevel=2, corrupted=True),
    ]
    # Vaal Orb outcomes:
    # 1/8 +1 Level
    # 1/8 -1 Level
    # 1/8 +Quality (up to 23) -> effectively same level
    # 1/8 -Quality -> effectively same level
    # 4/8 Nothing (Corrupted) -> same level
    # So:
    # Level 4: 1/8
    # Level 3: 6/8
    # Level 2: 1/8
    probabilities = [1/8, 6/8, 1/8]
    return TransformationRule(
        ingredients=ingredients, 
        products=products, 
        probabilities=probabilities, 
        info=f"Regular Vaal {item_name}",
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
    # Buy Lvl 1, use GCPs to 20%? No, exceptional gems don't need quality for leveling usually.
    # But maybe "5waygcp" implies leveling in 5-way with GCPs?
    # Original code: 20 GCPs.
    ingredients = [
        Ingredient(query=ItemQuery(name=item_name, gemLevel=1, corrupted=False), quantity=1),
        Ingredient(query=ItemQuery(name="Gemcutter's Prism"), quantity=20),
        Ingredient(query=ItemQuery(name="5waygcp"), quantity=1) # Service cost
    ]
    products = [
        ItemQuery(name=item_name, gemLevel=3, gemQuality=20, corrupted=False),
    ]
    probabilities = [1.0]
    return TransformationRule(
        ingredients=ingredients,
        products=products,
        probabilities=probabilities,
        info=f"GCP leveling {item_name}",
        tags=['scheme', 'leveling']
    )


def regular_level_exceptional(item_name):
    ingredients = [
        Ingredient(query=ItemQuery(name=item_name, gemLevel=1, corrupted=False), quantity=1),
        Ingredient(query=ItemQuery(name="5way"), quantity=1) # Service cost
    ]
    products = [
        ItemQuery(name=item_name, gemLevel=3, corrupted=False),
    ]
    probabilities = [1.0]
    return TransformationRule(
        ingredients=ingredients, 
        products=products, 
        probabilities=probabilities, 
        info=f"Regular leveling {item_name}"
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
        ingredients=[Ingredient(query=ItemQuery(name=TRANSMUTE), quantity=1)],
        products=[ItemQuery(name=PORTAL)],
        probabilities=[1.0],
        info="Convert Transmutes to Portals",
        multiplier=4, # 1 Transmute -> 4 Portals
    )

def the_dragons_heart():
    ingredients = [Ingredient(query=ItemQuery(name="The Dragon's Heart"), quantity=11)]
    products = [
        ItemQuery(name="Empower Support", gemLevel=4, corrupted=True)
    ]
    probabilities = [1.0]
    return TransformationRule(
        ingredients=ingredients, 
        products=products, 
        probabilities=probabilities, 
        multiplier=1/11, 
        info="The Dragon's Heart",
        tags=['divination_card', 'empower']
    )

def the_artist():
    ingredients = [Ingredient(query=ItemQuery(name="The Artist"), quantity=11)]
    products = [
        ItemQuery(name="Enhance Support", gemLevel=4, corrupted=True)
    ]
    probabilities = [1.0]
    return TransformationRule(
        ingredients=ingredients, 
        products=products, 
        probabilities=probabilities, 
        multiplier=1/11, 
        info="The Artist",
        tags=['divination_card', 'enhance']
    )

def wealth_and_power():
    ingredients = [Ingredient(query=ItemQuery(name="Wealth and Power"), quantity=11)]
    products = [
        ItemQuery(name="Enlighten Support", gemLevel=4, corrupted=True)
    ]
    probabilities = [1.0]
    return TransformationRule(
        ingredients=ingredients, 
        products=products, 
        probabilities=probabilities, 
        multiplier=1/11, 
        info="Wealth and Power",
        tags=['divination_card', 'enlighten']
    )


def vivid_watcher_reroll():
    awakened_gems = [
        "Awakened Added Chaos Damage Support",
        "Awakened Added Cold Damage Support",
        "Awakened Added Fire Damage Support",
        "Awakened Added Lightning Damage Support",
        "Awakened Brutality Support",
        "Awakened Burning Damage Support",
        "Awakened Cold Penetration Support",
        "Awakened Controlled Destruction Support",
        "Awakened Deadly Ailments Support",
        "Awakened Elemental Damage with Attacks Support",
        "Awakened Elemental Focus Support",
        "Awakened Fire Penetration Support",
        "Awakened Lightning Penetration Support",
        "Awakened Melee Physical Damage Support",
        "Awakened Melee Splash Support",
        "Awakened Minion Damage Support",
        "Awakened Swift Affliction Support",
        "Awakened Unbound Ailments Support",
        "Awakened Vicious Projectiles Support",
        "Awakened Void Manipulation Support",
        "Awakened Ancestral Call Support",
        "Awakened Arrow Nova Support",
        "Awakened Blasphemy Support",
        "Awakened Cast On Critical Strike Support",
        "Awakened Cast While Channelling Support",
        "Awakened Chain Support",
        "Awakened Fork Support",
        "Awakened Generosity Support",
        "Awakened Greater Multiple Projectiles Support",
        "Awakened Hextouch Support",
        "Awakened Increased Area of Effect Support",
        "Awakened Multistrike Support",
        "Awakened Spell Cascade Support",
        "Awakened Spell Echo Support",
        "Awakened Unleash Support"
    ]
    
    ingredients = [
        Ingredient(query=ItemQuery(name="Vivid Watcher"), quantity=1),
        Ingredient(query=ItemQuery(name="Cheapest Awakened Gem"), quantity=1)
    ]
    
    products = [
        ItemQuery(name=name, gemLevel=1, corrupted=False)
        for name in awakened_gems
    ]
    
    return TransformationRule(
        ingredients=ingredients,
        products=products,
        probabilities=[1/len(products)] * len(products),
        multiplier=1,
        info="Vivid Watcher Reroll",
        tags=['beast', 'gamble', 'awakened_gem']
    )

def wild_brambleback_leveling(gem_name):
    ingredients = [
        Ingredient(query=ItemQuery(name=gem_name, gemLevel=1, corrupted=False), quantity=1),
        Ingredient(query=ItemQuery(name="Wild Brambleback"), quantity=4)
    ]
    products = [
        ItemQuery(name=gem_name, gemLevel=5, corrupted=False)
    ]
    return TransformationRule(
        ingredients=ingredients,
        products=products,
        probabilities=[1.0],
        multiplier=1,
        info=f"Wild Brambleback Leveling: {gem_name}",
        tags=['beast', 'leveling']
    )

if __name__ == "__main__":
    # Fetch prices
    prices = retrieve_prices(["SkillGem", "DivinationCard", "Currency"])
    
    # Convert raw ninja prices to Valuations (or just dicts that PriceStore can handle)
    # HashKeyPriceStore expects Valuations.
    # But we can also just use a list of dicts if we adapt it.
    # My updated HashKeyPriceStore expects Valuations.
    
    from poe.valuation.framework.valuation import Valuation
    import pendulum
    
    valuations = []
    for category, items in prices.items():
        for item in items:
            # Convert ninja item to Valuation
            # Ninja item has: name, chaosValue, gemLevel, gemQuality, corrupted, etc.
            
            # Map ninja keys to ItemQuery keys
            query = ItemQuery(
                name=item.get('name'),
                type=item.get('type'), # Ninja might not have this
                gemLevel=item.get('gemLevel'),
                gemQuality=item.get('gemQuality'),
                corrupted=item.get('corrupted'),
                links=item.get('links'),
                baseType=item.get('baseType')
            )
            
            val = Valuation(
                key=query,
                estimate=item.get('chaosValue', 0),
                timestamp=pendulum.now().int_timestamp,
                tags=[category],
                info=item.get('name')
            )
            valuations.append(val)
            
    # Add custom prices
    valuations.append(Valuation(key=ItemQuery(name="5way"), estimate=400/39, timestamp=0, tags=['custom'], info="5way"))
    valuations.append(Valuation(key=ItemQuery(name="5waygcp"), estimate=400/78, timestamp=0, tags=['custom'], info="5waygcp"))
    valuations.append(Valuation(key=ItemQuery(name="Doryani's Institute"), estimate=100, timestamp=0, tags=['custom'], info="Doryani's Institute")) # Dummy price

    price_store = HashKeyPriceStore(valuations)
    manifester = Manifester(price_store)
    
    rules = (
            level_exceptional()
            + vaal_exceptional()
            + [terrible_secret_of_space(), gemcutters_mercy(), portal_scroll(), the_dragons_heart(), the_artist(), wealth_and_power()]
    )
    
    outcomes = []
    for rule in rules:
        outcome = manifester.manifest(rule)
        outcomes.append(outcome)
        print(f"{outcome.info}")
