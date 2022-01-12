import json
from pathlib import Path

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from poe.ninja import retrieve_prices
from poe.trade.exchange_resolver import ExchangeResolver
from poe.trade.listings_resolver import ListingsResolver
from poe.trade_finder import find_profitable_items, create_queries, generate_whisper
import pandas as pd

from poe.trade_finder.whisper_generator import translate_currency, fill_in_whisper_amounts
from trades.models import Item


def profitable_items(request):
    prices = retrieve_prices()
    obj, created = Item.objects.update_or_create(name="Exalted Orb", price=prices["Exalted Orb"][0]["chaosValue"])
    obj, created = Item.objects.update_or_create(name="Chaos Orb", price=1)
    items: pd.DataFrame = find_profitable_items(prices)
    items["icon"] = items.index.map(lambda x: prices[x][0].get("icon"))
    items["explicit_mods"] = items.index.map(lambda x: prices[x][0].get("explicitModifiers"))
    result = list(items.reset_index().T.to_dict().values())
    return JsonResponse(result, safe=False)


def whispers(request):
    exchange_resolver = ExchangeResolver()
    listings_resolver = ListingsResolver()
    items = pd.DataFrame(json.loads(request.body)).rename({"name": "index"}, axis=1).set_index("index")

    key_mapping = pd.read_csv(f"{Path(__file__).resolve().parent}/poe_keys.csv").set_index("name")["key"]
    reverse_mapping = {v: k for k, v in key_mapping.items()}
    prices = {item.name: [{"chaosValue": item.price}] for item in Item.objects.all()}
    df = items.reset_index()
    df = create_queries(df, key_mapping)
    df["trade_hash_json"] = df['query'].apply(exchange_resolver.resolve)
    whispers = pd.concat(df.trade_hash_json.apply(listings_resolver.resolve).values.tolist(), ignore_index=True)
    whispers["value"] = whispers.get_currency.map(reverse_mapping).map(items.value)
    whispers = translate_currency(whispers, prices)
    whispers = fill_in_whisper_amounts(whispers)
    result = list(whispers.T.to_dict().values())
    return JsonResponse(result, safe=False)
