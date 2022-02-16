import json
from pathlib import Path

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from constants import LEAGUE
from poe.ninja import retrieve_prices
from poe.sale.inventory_creator import create_inventory
from poe.trade.exchange_resolver import ExchangeResolver
from poe.trade.listings_resolver import ListingsResolver
import pandas as pd

from poe.trade.search_resolver import SearchResolver
from poe.trade_finder import find_profitable_items
from poe.trade_finder.whisper_generator import WhisperGenerator, exchange_parser
from poe.valuation import own_valuations
from poe.valuation.gems.experience import xp_value
from trades.models import Item


def profitable_items(request):
    prices = retrieve_prices()
    obj, created = Item.objects.update_or_create(name="Exalted Orb", price=prices["Exalted Orb"][0]["chaosValue"])
    obj, created = Item.objects.update_or_create(name="Chaos Orb", price=1)
    values = own_valuations(prices)
    items: pd.DataFrame = find_profitable_items(prices, values)
    items["icon"] = items.index.map(lambda x: prices.get(x, [{"icon": ""}])[0].get("icon"))
    items["explicit_mods"] = items.index.map(
        lambda x: prices.get(x, [{"explicitModifiers": [""]}])[0].get("explicitModifiers")
    )
    result = list(items.reset_index().T.to_dict().values())
    return JsonResponse(result, safe=False)


def whispers(request):
    items = (
        pd.DataFrame(list(zip(*dict(request.GET).values())), columns=request.GET.keys())
            .rename({"name": "index"}, axis=1)
            .set_index("index")
    )
    items["expected_profit"] = items["expected_profit"].astype("float")
    items["value"] = items["value"].astype("float")
    prices = {item.name: [{"chaosValue": item.price}] for item in Item.objects.all()}
    key_mapping = pd.read_csv(f"{Path(__file__).resolve().parent}/poe_keys.csv").set_index("name")["key"]

    listings_resolver = ListingsResolver(league=LEAGUE)
    exchange_resolver = ExchangeResolver(league=LEAGUE)
    use_case = WhisperGenerator(
        exchange_resolver=exchange_resolver,
        listings_resolver=listings_resolver,
        poe_trade_key_mapping=key_mapping,
        prices=prices,
    )
    domain_result = use_case(items)
    result = list(domain_result.T.to_dict().values())
    return JsonResponse(result, safe=False)


def orb_of_horizons(request):
    query = {
        "exchange": {"status": {"option": "online"}, "have": ["chaos"], "want": ["orb-of-horizons"], "minimum": 100}
    }
    prices = retrieve_prices(["Currency"])
    listings_resolver = ListingsResolver(league=LEAGUE)
    exchange_resolver = ExchangeResolver(league=LEAGUE)
    temp = exchange_parser(listings_resolver.resolve(exchange_resolver.resolve(query)))
    temp["value"] = prices["Orb of Horizons"][0]["chaosValue"]
    temp["profit"] = (temp.value - temp.price) * temp.stock
    temp["whisper"] = temp.apply(lambda x: x["whisper_template"].format(x["stock"], x["stock"] * x["price"]), axis=1)
    result = list(temp.T.to_dict().values())
    return JsonResponse(result, safe=False)


def search_resolve(request):
    query = json.loads(request.body)
    search_resolver = SearchResolver(league=LEAGUE)
    listings_resolver = ListingsResolver(league=LEAGUE)
    temp = listings_resolver.resolve(search_resolver.resolve(query))
    result = temp
    return JsonResponse(result, safe=False)


def gem_exp(request):
    prices = retrieve_prices(["SkillGem"])
    domain_result = xp_value(prices)[:30]
    domain_result['query'] = domain_result['name'].map(create_query)
    result = list(domain_result.T.to_dict().values())
    return JsonResponse(result, safe=False)


def gem_vaal(request):
    prices = retrieve_prices(["SkillGem"])
    gems = [item for price in prices.values() for item in price if item["type"] == "SkillGem"]
    df = pd.DataFrame(gems)
    assign_types = (lambda x: 'special' if any(y in x for y in (
        'Enhance Support', 'Enlighten Support', 'Empower Support')) else 'Awakened' if 'Awakened' in x else 'normal')
    funcs = {
        'special': lambda row: row['4c'] * (1 / 8) + row['2c'] * (1 / 8) + row['3c'] * 6 / 8 - row['3'],
        'Awakened': lambda row: row['6c'] * (1 / 8) + row['4c'] * (1 / 8) + row.get('5c', 0) * 6 / 8 - row.get('5',
                                                                                                               1000),
        'normal': lambda row: row['21c'] * (1 / 8) + row.get('19c', 0) * (1 / 8) + row['20c'] * 6 / 8 - row['20'],
    }

    def map_to_value(row):
        return funcs[assign_types(row.name)](row)

    pivoted_gems = df.pivot(index='name', columns='variant', values='chaosValue')
    domain_result = pivoted_gems.apply(map_to_value, axis=1).sort_values(ascending=False).reset_index()
    domain_result.columns = ['name', 'profit']
    domain_result = domain_result.dropna()
    result = {'result': list(domain_result.T.to_dict().values())}
    return JsonResponse(result, safe=False)


def create_query(name):
    alternate_qualities = {"anomalous": "1", "divergent": "2", "phantasmal": "3"}
    if (prefix := name.split()[0].lower()) in alternate_qualities:
        processed_name = name[len(prefix):].strip()
    else:
        processed_name = name
    query = {'query': {
        "status": {
            "option": "online"
        },
        "type": processed_name,
        "stats": [
            {
                "type": "and",
                "filters": []
            }
        ],
        "filters": {
            "misc_filters": {
                "disabled": False,
                "filters": {
                    "gem_level": {
                        "min": 1,
                        "max": 1
                    },
                    "corrupted": {
                        "option": "false"
                    },
                    'gem_alternate_quality': {'option': alternate_qualities.get(prefix, "0")}

                }
            }
        }
    }}
    return query


def register(request):
    prices = retrieve_prices()
    domain_result = create_inventory(prices)
    domain_result['final_price_numerator'] = domain_result.final_price.map(lambda x: x.numerator)
    domain_result['final_price_denominator'] = domain_result.final_price.map(lambda x: x.denominator)
    domain_result = domain_result.drop('final_price', axis=1)

    result = {'result': list(domain_result.T.to_dict().values())}
    return JsonResponse(result, safe=False)
