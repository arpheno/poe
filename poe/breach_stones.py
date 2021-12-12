import pandas as pd

from poe.ninja import retrieve_prices


def breach_stones():
    prices = retrieve_prices(["Fragment", "Currency"])
    breach_stones = pd.DataFrame(
        [
            (key.split("'")[0], key.split()[1], value[0]["chaosValue"])
            for key, value in prices.items()
            if "Breachstone" in key
            if not "lawless" in key
        ]
    )
    charge_map = {"Breachstone": 0, "Charged": 1, "Enriched": 2, "Pure": 3}
    breach_stones[1] = breach_stones[1].map(charge_map)
    blessings = pd.Series(
        {key.split()[-1]: value[0]["chaosValue"] for key, value in prices.items() if "Blessing of" in key}
    )
    breach_stones["blessing"] = breach_stones.apply(lambda x: blessings[x[0]], axis=1)
    breach_stones["cost"] = breach_stones.apply(lambda x: x[2] + (3 - x[1]) * x["blessing"], axis=1)
    breach_stones.groupby(by=0)

    breach_stones = breach_stones.set_index(0).join(
        breach_stones[[0, 1, "cost"]]
        .groupby(by=0)
        .apply(lambda df: df[df[1] == 3])
        .set_index(0)
        .drop(1, axis=1)
        .rename({"cost": "value"}, axis=1),
        how="outer",
    )
    breach_stones["profit"] = breach_stones["value"] - breach_stones["cost"]
    breach_stones = breach_stones[[1, "profit", "value", "cost", "blessing"]].reset_index().sort_values([1, 0])
    breach_stones[1] = breach_stones[1].map({value: key for key, value in charge_map.items()})
    breach_stones.style.background_gradient(axis=1)
    return breach_stones[breach_stones["profit"] > 0]