import time

import requests

from poe.headers import headers
from poe.timeless.query import query_timeless_jewel


def find_doryiani(seed: int, name_of="timeless"):

    data = query_timeless_jewel(name_of, seed)
    response = requests.post("https://www.pathofexile.com/api/trade/search/Scourge", headers=headers, json=data)
    # if response.json()['result']:
    if response.status_code == 429:
        print("too fast (")
    time.sleep(5)
    result = response.json()
    result_hash = result["id"]
    if result["result"]:
        print(f"https://www.pathofexile.com/trade/search/Scourge/{result_hash}")
    return result_hash