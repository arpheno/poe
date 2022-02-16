import json
import math
from collections import ChainMap
from fractions import Fraction

import pandas as pd

from constants import hard_currency
from poe.item.item_builder import build_items
from poe.item.type_determiner import type_mapping
from poe.ninja import retrieve_prices
from poe.valuation import own_valuations


def main(prices):
    valuations = pd.Series(own_valuations(prices))
    type_mapper = type_mapping(prices)
    items = build_items(prices, type_mapper)
    df = pd.DataFrame(
        [
            dict(
                chaos_value=item.value,
                type=item.type,
                type_line=item.typeLine,
                initial_price=item.price,
                shoplink_template=item.shoplink_template,
                stack_size=item.stack_size,
            )
            for item in items
        ]
    )
    df["simple_value"] = pd.concat([df.type_line.map(valuations),df.initial_price],axis=1).max(axis=1)
    df["config_value"] = df.simple_value * df.stack_size

    df["type"] = df.type_line.map(
        {**(df.set_index("type_line")["type"].to_dict()), **{x: "Hard Currency" for x in hard_currency}}
    )
    # set chaos value equal to stacksize
    df.loc[df.type_line == "Chaos Orb", "chaos_value"] = df.loc[df.type_line == "Chaos Orb", "stack_size"]
    #Some cleaning for none types and worthless items
    inventory = df[~df["type"].isin([None]) & (df.chaos_value > 0)]

    register = inventory.copy()
    register["temp_up_priced_value_fx"] = register.apply(up_price, axis=1)
    register["up_priced_value_fx"] = register[["temp_up_priced_value_fx", "config_value"]].max(axis=1)
    register["final_price"] = register.apply(
        lambda self: Fraction(self.up_priced_value_fx / self.stack_size).limit_denominator(self.stack_size), axis=1
    )
    register = register.query('type != "Hard Currency"')
    register = register.query('chaos_value > 10')
    return register
    # content = list(_register.apply(lambda row: row.shoplink_template.format(**row), axis=1))


def keywords(words, mult):
    return lambda item: mult if any(word in item.type_line for word in words) else 1


onefive = ["inged"]


def up_price(item):
    base = 1.4
    if item.type_line == "Offering to the Goddess":
        base = base
    if item.type in ("SkillGem", "Base", "Prophecy"):
        base = 0.90
    base *= keywords(onefive, 1.35)(item)
    if item.type == "Resonator":
        base = 3

    if item.type == "Incubator":
        base *= 1.5
    if item.type == "Catalyst" and item.stack_size < 10:
        base *= 5
    else:
        base *= 1
    if item.stack_size > 50:
        base *= 1.1

    return math.ceil(base * item.chaos_value)


if __name__ == "__main__":

    prices = retrieve_prices()

    domain_result=main(prices)
    domain_result['numerator']=domain_result.final_price.map(lambda x:x.numerator)
    domain_result['denominator']=domain_result.final_price.map(lambda x:x.numerator)
    domain_result.drop('final_price',axis=1)
    domain_result = domain_result.drop('final_price', axis=1)

    result = {'result': list(domain_result.T.to_dict().values())}
    assert json.loads(json.dumps(result))
