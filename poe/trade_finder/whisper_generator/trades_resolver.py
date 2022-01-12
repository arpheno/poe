import logging

import pandas as pd

from poe.trade.listings_resolver import ListingsResolver

min_profit = 5
logger = logging.getLogger(__name__)
default_return = pd.DataFrame(
    columns=["pay_currency", "get_currency", "price", "stock", "id", "whisper_template", "value", "profit", "whisper"]
)


