import json
from fractions import Fraction

import pandas as pd

from poe.ninja import retrieve_prices
from poe.sale.inventory_management_builder import build_inventory_management
from poe.trade.stash_tabs.all_tabs_getter import get_all_tabs
from poe.valuation import own_valuations


if __name__ == "__main__":

    price_markup_by_type = {
        "SkillGem": 0.9,
        "Base": 0.9,
        "Resonator": 3,
        "Incubator": 1.5,
    }
    base_price_markup = 1.6
    cleaning_rules = ['type != "Hard Currency"', "config_value > 10"]
    thread = "3231447"
    prices = retrieve_prices()
    valuations = pd.Series(own_valuations(prices))

    use_case = build_inventory_management(
        prices=prices,
        valuations=valuations,
        price_base_by_type=price_markup_by_type,
        price_base=base_price_markup,
        cleaning_rules=cleaning_rules,
        thread=thread,
    )
    raw_items = get_all_tabs(25)
    inventory = use_case.create_inventory(raw_items)
    sales_proposition = use_case.sales_proposition(inventory)

    # domain_result["numerator"] = domain_result.final_price.map(lambda x: x.numerator)
    # domain_result["denominator"] = domain_result.final_price.map(lambda x: x.numerator)
    # domain_result.drop("final_price", axis=1)
    # domain_result = domain_result.drop("final_price", axis=1)

    # result = {"result": list(domain_result.T.to_dict().values())}
    # assert json.loads(json.dumps(result))
