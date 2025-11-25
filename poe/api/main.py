from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import pendulum

from poe.valuation.framework.new_rules import (
    level_exceptional, vaal_exceptional, terrible_secret_of_space, 
    gemcutters_mercy, portal_scroll, the_dragons_heart, the_artist, wealth_and_power,
    vivid_watcher_reroll, wild_brambleback_leveling
)
from poe.valuation.framework.manifester import Manifester
from poe.valuation.framework.price_store import HashKeyPriceStore
from poe.valuation.framework.models import ItemQuery
from poe.valuation.framework.valuation import Valuation
from poe.ninja import retrieve_prices
from poe.constants import LEAGUE
from poe.trade.proxy_listings_resolver import ListingsResolver
from poe.trade.proxy_search_resolver import SearchResolver
from poe.woke.mod_mapper import ModMapper
from poe.woke.query_builder import build_query
from poe.api.client import client
from poe.trade.prices import get_doryani_institute_price, get_vivid_watcher_price, get_wild_brambleback_price

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Trade Search Setup ---
PROXY_BASE_URL = "http://localhost:8999"
search_resolver = SearchResolver(league=LEAGUE, base_url=PROXY_BASE_URL)
listings_resolver = ListingsResolver(league=LEAGUE, base_url=PROXY_BASE_URL)

trade_keys = None
mod_mapper = None

def get_mod_mapper():
    global trade_keys, mod_mapper
    if trade_keys is None:
        # Use our client to fetch stats
        response = client.get("/api/trade/data/stats")
        trade_keys = response.json()
        mod_mapper = ModMapper(trade_keys)
    return mod_mapper

def to_chaos(price: dict) -> float:
    """Convert price to chaos equivalent"""
    currency = price.get('currency')
    amount = price.get('amount', 0)
    if currency == 'chaos':
        return amount
    elif currency == 'divine':
        return amount * 150 # TODO: Fetch from ninja
    return 0

class SearchRequest(BaseModel):
    type: str = ""
    prefixes: List[str] = []
    suffixes: List[str] = []
    misc: dict = {}

@app.post("/search")
def search(request: SearchRequest):
    try:
        mapper = get_mod_mapper()
        
        all_mods = request.prefixes + request.suffixes
        
        query_args = {}
        if all_mods:
            query_args['mods'] = mapper.map_mods('explicit', all_mods)
        
        if request.type:
            query_args['type'] = request.type
            
        if request.misc:
            query_args['misc'] = request.misc
            
        query = build_query(**query_args)
        search_params = search_resolver.resolve(query)
        results = listings_resolver.resolve(search_params)
        
        listings = []
        for item in results.get('result', []):
            listing = {
                'id': item.get('id'),
                'item': item.get('item', {}),
                'listing': item.get('listing', {}),
            }
            
            if 'price' in item.get('listing', {}):
                price = item['listing']['price']
                listing['chaos_price'] = to_chaos(price)
            
            listings.append(listing)
            
        return {
            'success': True,
            'count': len(listings),
            'results': listings,
            'query': query
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}

# --- Valuation Setup ---

class BreakdownItem(BaseModel):
    name: str
    quantity: Optional[int] = None
    probability: Optional[float] = None
    unit_cost: Optional[float] = None
    total_cost: Optional[float] = None
    unit_value: Optional[float] = None
    expected_revenue: Optional[float] = None

class Breakdown(BaseModel):
    ingredients: List[BreakdownItem]
    products: List[BreakdownItem]
    cost: float
    revenue: float
    profit: float
    multiplier: float
    scaled_profit: float

class Opportunity(BaseModel):
    name: str
    profit: float
    cost: float
    roi: float
    risk: float
    tags: List[str]
    breakdown: Optional[Breakdown] = None

@app.get("/opportunities", response_model=List[Opportunity])
def get_opportunities():
    # Fetch prices (cached?)
    # Ideally we should cache this or run it in a background task.
    # For now, let's fetch on demand (slow) or use a global cache.
    
    prices = retrieve_prices(["SkillGem", "DivinationCard", "Currency"])
    
    valuations = []
    for category, items in prices.items():
        for item in items:
            # Only default corrupted to False for Skill Gems, as Divination Cards don't have this property
            corrupted = item.get('corrupted')
            if item.get('type') == 'SkillGem' and corrupted is None:
                corrupted = False
                
            query = ItemQuery(
                name=item.get('name'),
                # type=item.get('type'),
                gemLevel=item.get('gemLevel'),
                gemQuality=item.get('gemQuality'),
                corrupted=corrupted,
                # links=item.get('links'),
                # baseType=item.get('baseType')
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
    
    doryani_price = get_doryani_institute_price()
    valuations.append(Valuation(key=ItemQuery(name="Doryani's Institute"), estimate=doryani_price, timestamp=0, tags=['custom'], info="Doryani's Institute"))

    vivid_watcher_price = get_vivid_watcher_price()
    valuations.append(Valuation(key=ItemQuery(name="Vivid Watcher"), estimate=vivid_watcher_price, timestamp=0, tags=['custom'], info="Vivid Watcher"))

    wild_brambleback_price = get_wild_brambleback_price()
    valuations.append(Valuation(key=ItemQuery(name="Wild Brambleback"), estimate=wild_brambleback_price, timestamp=0, tags=['custom'], info="Wild Brambleback"))

    # Calculate cheapest awakened gem
    cheapest_awakened_gem_price = float('inf')
    
    # Store gem prices for leveling calculation
    gem_prices = {} # name -> {level -> price}
    
    for items in prices.values():
        for item in items:
            if item.get('type') == 'SkillGem':
                name = item.get('name')
                level = item.get('gemLevel')
                corrupted = item.get('corrupted')
                price = item.get('chaosValue', 0)
                
                if not corrupted:
                    if name not in gem_prices:
                        gem_prices[name] = {}
                    gem_prices[name][level] = price

                if name.startswith('Awakened') and level == 1 and not corrupted:
                    if price < cheapest_awakened_gem_price:
                        cheapest_awakened_gem_price = price
    
    if cheapest_awakened_gem_price == float('inf'):
        cheapest_awakened_gem_price = 0 # Fallback or handle error

    valuations.append(Valuation(key=ItemQuery(name="Cheapest Awakened Gem"), estimate=cheapest_awakened_gem_price, timestamp=0, tags=['custom'], info="Cheapest Awakened Gem"))

    # Find top 3 gems for Wild Brambleback leveling
    brambleback_opportunities = []
    for name, levels in gem_prices.items():
        if 1 in levels and 5 in levels:
            price_lvl_1 = levels[1]
            price_lvl_5 = levels[5]
            cost = price_lvl_1 + (4 * wild_brambleback_price)
            profit = price_lvl_5 - cost
            brambleback_opportunities.append({
                'name': name,
                'profit': profit
            })
            
    brambleback_opportunities.sort(key=lambda x: x['profit'], reverse=True)
    top_3_brambleback = brambleback_opportunities[:3]
    
    brambleback_rules = [
        wild_brambleback_leveling(opp['name']) for opp in top_3_brambleback
    ]

    price_store = HashKeyPriceStore(valuations)
    manifester = Manifester(price_store)
    
    rules = (
            level_exceptional()
            + vaal_exceptional()
            + [terrible_secret_of_space(), gemcutters_mercy(), portal_scroll(), the_dragons_heart(), the_artist(), wealth_and_power(), vivid_watcher_reroll()]
            + brambleback_rules
    )
    
    opportunities = []
    for rule in rules:
        outcome = manifester.manifest(rule)
        
        # Hack: Parse the info string "Info | Profit: X | Risk: Y"
        try:
            parts = outcome.info.split("|")
            if len(parts) < 3:
                continue
                
            name = parts[0].strip()
            profit = float(parts[1].split(":")[1].strip())
            risk = float(parts[2].split(":")[1].strip())
            cost = outcome.estimate - profit
            roi = (profit / cost) * 100 if cost > 0 else 0
            
            opportunities.append(Opportunity(
                name=name,
                profit=profit,
                cost=cost,
                roi=roi,
                risk=risk,
                tags=outcome.tags,
                breakdown=outcome.breakdown
            ))
        except Exception as e:
            print(f"Error parsing outcome for {rule.info}: {e}")
            continue
            
    # Sort by profit
    opportunities.sort(key=lambda x: x.profit, reverse=True)
    
    return opportunities
