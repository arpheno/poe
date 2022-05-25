import numpy as np
import pandas as pd
from dataenforce import Dataset

from poe.trade.exchange_parser import exchange_parser


class WhisperGenerator:
    def __init__(
        self, exchange_resolver, listings_resolver, poe_trade_key_mapping, prices
    ):
        self.exchange_resolver = exchange_resolver
        self.listings_resolver = listings_resolver
        self.poe_trade_key_mapping = poe_trade_key_mapping
        self.reverse_mapping = {v: k for k, v in poe_trade_key_mapping.items()}
        self.prices = prices
        self.prices["Chaos Orb"] = [{"chaosValue": 1}]

    def __call__(self, df: Dataset["value":float, "expected_profit":float]):
        df = self.create_queries(df, self.poe_trade_key_mapping)
        whispers_stacked = (
            df["query"]
            .apply(self.exchange_resolver.resolve)
            .apply(exchange_parser)
        )
        whispers = pd.concat(whispers_stacked.values.tolist(), ignore_index=True)
        whispers["value"] = whispers.get_currency.map(self.reverse_mapping).map(
            df.value
        )
        whispers = self.translate_currency(whispers, self.prices)
        whispers = self.fill_in_whisper_amounts(whispers)
        return whispers

    def fill_in_whisper_amounts(self, whispers):
        whispers["profit"] = (
            whispers["value"] - whispers["chaos_price"]
        ) * whispers.stock
        whispers["relative_profit"] = whispers.profit / whispers.chaos_price
        whispers["whisper"] = whispers.apply(
            lambda row: row["whisper_template"].format(
                row["stock"], row.price * row.stock
            ),
            axis=1,
        )
        whispers = whispers.query("chaos_price < value")
        print(f'Found {len(whispers)} results with {whispers["profit"].sum()} profit')
        print(whispers[["pay_currency", "price", "chaos_price"]])
        return whispers

    def query(self, want, minimum):
        return {
            "engine":'new',
            "status": {"option": "online"},
            "query": {
                "have": ["chaos", "exalt"],
                "want": [want],
                "minimum": minimum,
            }
        }

    def translate_currency(self, df, prices):
        df["pay_currency"] = df["pay_currency"].map(
            {"chaos": "Chaos Orb", "exalted": "Exalted Orb"}
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

#
# if __name__ == "__main__":
#     prices = retrieve_prices()
#     key_mapping = pd.read_csv(f"{Path(__file__).resolve().parent}/poe_keys.csv").set_index("name")["key"]
#     exchange_resolver = ExchangeResolver()
#     listings_resolver = ListingsResolver()
#     use_case = WhisperGenerator(
#         exchange_resolver=exchange_resolver,
#         listings_resolver=listings_resolver,
#         poe_trade_key_mapping=key_mapping,
#         prices=prices,
#     )
#     s = pd.DataFrame(
#         {
#             "value": {"The Artist": 180.49},
#             "expected_profit": {"The Artist": 130.49},
#         }
#     )
#     whispers = use_case(s)
#     print(whispers)
