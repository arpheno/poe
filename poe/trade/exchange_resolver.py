import time

import requests
from redislite import Redis

from poe.trade.exchange_response import ExchangeResponse
from poe.trade.headers import headers
from poe.trade.rate_limiter import limit_rate


class ExchangeResolver:
    def __init__(self, league="Standard", cache=Redis()):
        self.league = league
        self.cache = cache
        self.url = f"https://www.pathofexile.com/api/trade/exchange/{league}"

    def resolve(self, query) -> dict[str, list[tuple[str, str]]]:
        key = "trade-exchange-request-limit"
        limits = ["7:15:60", "15:90:120", "45:300:1800", "3:5:60"]
        with limit_rate(key, limits, self.cache):
            response = requests.post(self.url, headers=headers, json=query)
        if response.status_code == 429:
            print(f"too fast {response.headers}")
            time.sleep(120)
            return self.resolve(query)
        result = response.json()
        result["result"] = [value for value in result["result"].values()]
        exchange_result = ExchangeResponse(**result)
        return exchange_result
