import logging
import time

import pandas as pd
import requests
from redislite import Redis

from poe.trade.headers import headers
from poe.trade.rate_limiter import limit_rate

logger = logging.getLogger(__file__)


class ListingsResolver:
    def __init__(self, league="Standard", cache=Redis()):
        self.league = league
        self.cache = cache
        self.url = f"https://www.pathofexile.com/api/trade/exchange/{league}"

    def resolve(self,result) -> tuple[str, dict]:
        key = "'trade-fetch-request-limit'"
        limits = ["6:4:10", "12:4:60", "16:12:60"]
        params = [
            (
                "query",
                result['id'],
            ),

            ("exchange", ""),
            # ('pseudos[]',['pseudo.pseudo_total_life', 'pseudo.pseudo_number_of_crafted_suffix_mods', 'pseudo.pseudo_number_of_suffix_mods'])
        ]
        with limit_rate(key, limits, self.cache):
            response = requests.get(
                f'https://www.pathofexile.com/api/trade/fetch/{",".join(result["result"][:20])}',
                headers=headers,
                params=params,
            )
        if response.status_code == 429:
            print(f"too fast {response.headers}")
            time.sleep(60)
            return self.resolve(result)
        return response.json()



