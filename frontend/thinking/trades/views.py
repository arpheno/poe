import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from poe.ninja import retrieve_prices
from poe.trade_finder import find_profitable_items, generate_whispers, generate_whisper
import pandas as pd


def profitable_items(request):
    prices = retrieve_prices()
    items: pd.DataFrame = find_profitable_items(prices)
    result = list(find_profitable_items(prices).reset_index().T.to_dict().values())
    return JsonResponse(result, safe=False)


def whispers(request):
    items= pd.DataFrame(json.loads(request.body)).rename({'name':'index'},axis=1).set_index('index')
    whispers=generate_whisper(items)
    result=list(whispers.T.to_dict().values())
    return JsonResponse(result, safe=False)
