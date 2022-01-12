import logging
import time

import pandas as pd
import requests
from redislite import Redis

from poe.trade.headers import headers
from poe.trade.rate_limiter import limit_rate

logger = logging.getLogger(__file__)


class ListingsResolver:
    def __init__(self, league="Scourge", cache=Redis()):
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
        if response.json().get("result"):
            df = pd.DataFrame(
                [
                    {
                        "pay_currency": result["listing"]["price"]["exchange"]["currency"],
                        "get_currency": result["listing"]["price"]["item"]["currency"],
                        "price": result["listing"]["price"]["exchange"]["amount"]
                        / result["listing"]["price"]["item"]["amount"],
                        "stock": result["listing"]["price"]["item"]["stock"],
                        "id": result["id"],
                        "whisper_template": result["listing"]["whisper"],
                    }
                    for result in response.json()["result"]
                ]
            )
        else:
            df = pd.DataFrame(columns=["pay_currency", "get_currency", "price", "stock", "id", "whisper_template"])
        return df


def resolve_listings(hash, result):
    params = [
        (
            "query",
            hash,
        ),
        ("exchange", ""),
    ]
    response = requests.get(
        f'https://www.pathofexile.com/api/trade/fetch/{",".join(result[:20])}',
        headers=headers,
        params=params,
    )
    if response.json().get("result"):
        df = pd.DataFrame(
            [
                {
                    "pay_currency": result["listing"]["price"]["exchange"]["currency"],
                    "get_currency": result["listing"]["price"]["item"]["currency"],
                    "price": result["listing"]["price"]["exchange"]["amount"]
                    / result["listing"]["price"]["item"]["amount"],
                    "stock": result["listing"]["price"]["item"]["stock"],
                    "id": result["id"],
                    "whisper_template": result["listing"]["whisper"],
                }
                for result in response.json()["result"]
            ]
        )
    else:
        df = pd.DataFrame(columns=["pay_currency", "get_currency", "price", "stock", "id", "whisper_template"])
    return df
