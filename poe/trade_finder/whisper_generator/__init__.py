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
