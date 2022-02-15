import time

import requests
from redislite import Redis

from poe.trade.headers import headers
from poe.trade.rate_limiter import limit_rate


class SearchResolver:
    def __init__(self, league="Standard", cache=Redis()):
        self.league = league
        self.cache = cache
        self.url = f"https://www.pathofexile.com/api/trade/search/{league}"

    def resolve(self, query) -> dict:
        key = "trade-exchange-request-limit"
        limits = ["8:10:60", "15:60:120", "60:300:1800", "3:5:60"]
        with limit_rate(key, limits, self.cache):
            response = requests.post(self.url, headers=headers, json=query)
        if response.status_code == 429:
            print(f"too fast {response.headers}")
            time.sleep(120)
            return self.resolve(query)
        result = response.json()
        result_hash = result["id"]
        print(f"{self.url.replace('/api', '')}/{result_hash}")
        params = {
            "params": [
                (
                    "query",
                    result["id"],
                )
            ],
            "result": result["result"][:10],
        }

        return params
