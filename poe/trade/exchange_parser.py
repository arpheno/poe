import pandas as pd

from poe.trade.exchange_response import ExchangeResponse


def exchange_parser(data:ExchangeResponse):
    if data.results:
        df = pd.DataFrame(
            [
                {
                    "pay_currency": result.listing.offers[0].exchange.currency,
                    "get_currency": result.listing.offers[0].item.currency,
                    "price": result.listing.offers[0].exchange.amount
                    / result.listing.offers[0].item.amount,
                    "stock": result.listing.offers[0].item.stock,
                    "id": result.id,
                    "whisper_template": result.listing.whisper.format(result.listing.offers[0].item.whisper,result.listing.offers[0].exchange.whisper.replace('{0}','{1}')),
                    "whisper_token": result.listing.whisper_token,
                    "offer_count":result.listing.offers[0].item.stock//result.listing.offers[0].item.amount
                }
                for result in data.result
            ]
        )
    else:
        df = pd.DataFrame(
            columns=[
                "pay_currency",
                "get_currency",
                "price",
                "stock",
                "id",
                "whisper_template",
            ]
        )
    return df