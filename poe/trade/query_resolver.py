import time

import requests

from poe.trade.headers import headers


def resolve_query(query, league="Scourge"):
    url = f"https://www.pathofexile.com/api/trade/search/{league}"
    response = requests.post(url, headers=headers, json=query)
    if response.status_code == 429:
        print("too fast (")
    time.sleep(5)
    result = response.json()
    result_hash = result["id"]
    if result["result"]:
        print(f"{url.replace('/api','')}/{result_hash}")
    return result_hash


def resolve_exchange(query, league="Scourge"):
    url = f"https://www.pathofexile.com/api/trade/exchange/{league}"
    response = requests.post(url, headers=headers, json=query)
    if response.status_code == 429:
        print("too fast (")
    time.sleep(5)
    result = response.json()
    result_hash = result["id"]
    if result["result"]:
        print(f"{url.replace('/api','')}/{result_hash}")
    return (result_hash, result["result"])
