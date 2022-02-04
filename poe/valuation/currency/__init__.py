import pandas as pd

from constants import (
    TRANSMUTE,
    AUGMENT,
    ALTERATION,
    JEWELLERS,
    CHROMATIC,
    FUSING,
    CHANCE,
    SCOUR,
    REGRET,
    ALCHEMY,
    BAUBLE,
    WHETSTONE,
)
from poe.ninja import retrieve_prices
UNMAKING='Orb of Unmaking'
vendor_recipes = pd.DataFrame(
    {
        TRANSMUTE: (1 / 4, AUGMENT),
        AUGMENT: (1 / 4, ALTERATION),
        ALTERATION: (1 / 2, JEWELLERS),
        # JEWELLERS: (1 / 3, CHROMATIC),
        JEWELLERS: (1 / 4, FUSING),
        FUSING: (1.0, CHANCE),
        CHANCE: (1 / 4, SCOUR),
        SCOUR: (1 / 2, REGRET),
        # REGRET: (1.0, ALCHEMY),
        CHROMATIC: (1.0, CHROMATIC),
        WHETSTONE: (1 / 8, BAUBLE),
        BAUBLE: (1.0, BAUBLE),
        ALCHEMY: (1.0, ALCHEMY),
        REGRET:(1/4,UNMAKING)
    }
).T


def currency_valuation(prices):
    value = pd.DataFrame(pd.Series({k: v[0]["chaosValue"] for k, v in prices.items() if k in vendor_recipes.index}))
    value[1] = vendor_recipes[1].map(value[0]) * vendor_recipes[0]
    value[2] = vendor_recipes[1].map(value[1]) * vendor_recipes[0]
    value[3] = vendor_recipes[1].map(value[2]) * vendor_recipes[0]
    value[4] = vendor_recipes[1].map(value[3]) * vendor_recipes[0]
    value["max"] = value.max(axis=1)
    value = value[[0, "max"]]
    value.columns = ["ninja", "max"]
    value = value.query("max>ninja")
    return value["max"].to_dict()


if __name__ == "__main__":
    prices = retrieve_prices(["Currency"])
    currency_valuation(prices)
