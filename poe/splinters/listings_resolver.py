import logging

import pandas as pd
import requests

from poe.trade.headers import headers
logger = logging.getLogger(__file__)



def resolve_listings(hash, result):
    params = (
        (
            "query",
            hash,
        ),
        ("exchange", ""),
    )
    response = requests.get(
        f'https://www.pathofexile.com/api/trade/fetch/{",".join(result[:20])}',
        headers=headers,
        params=params,
    )
    try:
        df = pd.DataFrame(
            [
                {
                    "pay_currency": result["listing"]["price"]["exchange"]["currency"],
                    "get_currency": result["listing"]["price"]["item"]["currency"],
                    "price": result["listing"]["price"]["exchange"]["amount"]
                             / result["listing"]["price"]["item"]["amount"],
                    "stock": result["listing"]["price"]["item"]["stock"],
                    "id": result["id"],
                    "whisper_template":result['listing']['whisper']
                }
                for result in response.json()["result"]
            ]
        )
    except Exception as e:
        logger.exception("something went wrong")
    return df