import json
from pathlib import Path

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from poe.ninja import retrieve_prices
from poe.trade.exchange_resolver import ExchangeResolver
from poe.trade.listings_resolver import ListingsResolver
import pandas as pd

from poe.trade_finder import find_profitable_items
from poe.trade_finder.whisper_generator import WhisperGenerator
from poe.valuation import own_valuations
from trades.models import Item


def profitable_items(request):
    prices = retrieve_prices()
    obj, created = Item.objects.update_or_create(name="Exalted Orb", price=prices["Exalted Orb"][0]["chaosValue"])
    obj, created = Item.objects.update_or_create(name="Chaos Orb", price=1)
    values = own_valuations(prices)
    items: pd.DataFrame = find_profitable_items(prices, values)
    items["icon"] = items.index.map(lambda x: prices[x][0].get("icon"))
    items["explicit_mods"] = items.index.map(lambda x: prices[x][0].get("explicitModifiers"))
    result = list(items.reset_index().T.to_dict().values())
    return JsonResponse(result, safe=False)


def whispers(request):
    items = (
        pd.DataFrame(list(zip(*dict(request.GET).values())), columns=request.GET.keys())
        .rename({"name": "index"}, axis=1)
        .set_index("index")
    )
    items['expected_profit']=items['expected_profit'].astype('float')
    items['value']=items['value'].astype('float')
    prices = {item.name: [{"chaosValue": item.price}] for item in Item.objects.all()}
    key_mapping = pd.read_csv(f"{Path(__file__).resolve().parent}/poe_keys.csv").set_index("name")["key"]

    listings_resolver = ListingsResolver()
    exchange_resolver = ExchangeResolver()
    use_case = WhisperGenerator(
        exchange_resolver=exchange_resolver,
        listings_resolver=listings_resolver,
        poe_trade_key_mapping=key_mapping,
        prices=prices,
    )
    domain_result = use_case(items)
    result = list(domain_result.T.to_dict().values())
    return JsonResponse(result, safe=False)
