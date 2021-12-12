import pandas as pd

from poe.ninja import retrieve_prices
from poe.trade.query_resolver import resolve_exchange


def splinter_query(splinter: str):
    splinter_template = {
        "exchange": {
            "status": {"option": "online"},
            "have": ["chaos"],
            "want": [f"splinter-{splinter.lower()}"],
            "minimum": 30,
        }
    }
    return splinter_template


def breach_splinters():
    prices = retrieve_prices(["Fragment"])
    splinters = pd.Series(
        {key.split()[-1]: value[0]["chaosValue"] for key, value in prices.items() if "Splinter of" in key}
    )
    breach_stones = pd.Series(
        {key.split("'")[0]: value[0]["chaosValue"] for key, value in prices.items() if "'s Breachstone" in key}
    )

    profitable_splinters: pd.Series = (breach_stones / 100 - splinters).where(lambda x: x > 0).dropna()
    print(profitable_splinters)
    for key in profitable_splinters.keys():
        # TODO: Adjust trade query for profit/trade
        print(f"Buy {key} between {splinters[key]} and {splinters[key]+profitable_splinters[key]}")
        hash, _ = resolve_exchange(splinter_query(key))
    profitable_splinters = profitable_splinters.rename({x: f"Splinter of {x}" for x in profitable_splinters.keys()})
    return profitable_splinters


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


if __name__ == "__main__":
    _temp = _breach_stones()
    print(_temp)
