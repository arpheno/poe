from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from poe.ninja import retrieve_prices
from poe.trade_finder import find_profitable_items
import pandas as pd


def profitable_items(request):
    prices = retrieve_prices()
    items: pd.DataFrame = find_profitable_items(prices)
    result= list(find_profitable_items(prices).reset_index().T.to_dict().values())
    return JsonResponse(result,safe=False)
