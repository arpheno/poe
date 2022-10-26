import numpy as np
import pandas as pd
from dataenforce import Dataset

from poe.trade.exchange_parser import exchange_parser

class WhisperGenerator:

    def __call__(self, df: Dataset["value":float, "expected_profit":float]):
        pass

    def fill_in_whisper_amounts(self, whispers):
        pass

    def query(self, want, minimum):
        return {
            "engine":'new',
            "status": {"option": "online"},
            "query": {
                "have": ["chaos", "div"],
                "want": [want],
                "minimum": minimum,
            }
        }

    def translate_currency(self, df, prices):
        df["pay_currency"] = df["pay_currency"].map(
            {"chaos": "Chaos Orb", "div": "Divine Orb"}
        )
        currency_map = {
            k: v[0]["chaosValue"]
            for k, v in prices.items()
            if k in df.pay_currency.to_list()
        }
        df["chaos_price"] = df.price * df.pay_currency.map(currency_map)
        return df

    def create_queries(
            self,
            df: Dataset["value":float, "expected_profit":float, ...],
            key_mapping,
            min_profit: float = 5,
    ):
        # print(f'Creating Queries {df["index"][0]}', end=", ")
        df["minimum"] = np.ceil(min_profit / df.expected_profit)
        df["want"] = df.index.map(key_mapping)
        df["query"] = df.apply(lambda x: self.query(x.want, x.minimum), axis=1)
        return df
