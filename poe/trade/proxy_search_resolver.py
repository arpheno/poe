import time

import requests
from redislite import Redis

from poe.trade.headers import headers
from poe.trade.rate_limiter import limit_rate


class SearchResolver:
    def __init__(self, league="Standard",base_url="https://www.pathofexile.com"):
        self.league = league
        self.url = f"{base_url}/api/trade/search/{league}"

    def resolve(self, query) -> dict:
        response = requests.post(self.url, headers=headers, json=query)
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
