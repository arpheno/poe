import logging
import time

import pandas as pd
import requests
from redislite import Redis

from poe.trade.headers import headers
from poe.trade.rate_limiter import limit_rate

logger = logging.getLogger(__file__)


class ListingsResolver:
    def __init__(self, league="Standard",base_url="https://www.pathofexile.com"):
        self.league = league
        self.url = f"{base_url}/api/trade/fetch"

    def resolve(self, params) -> dict:
        response = requests.get(
            f'{self.url}/{",".join(params["result"])}',
            headers=headers,
            params=params["params"],
        )
        return response.json()
