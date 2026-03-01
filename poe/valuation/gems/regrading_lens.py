import sys

sys.path.append("/home/dhokuav/poe")

from pathlib import Path
from pprint import pprint

import pandas as pd

from poe.ninja import retrieve_prices
from poe.valuation.gems.adps import  markov_adps

display = pd.options.display

display.max_columns = 1000
display.max_rows = 10000


# def regrading_lenses():


def secondary_regrading_lens(prices):
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    relevant_gems = [
        gem
        for gem in gems
        if "Support" in gem["name"]
        if not "wakened" in gem["name"]
        if gem["sparkline"]["data"]
        if not gem.get("corrupted")
        if gem["variant"] == "1"
    ]
    lens_cost = prices["Secondary Regrading Lens"][0]["chaosValue"]
    return regrading_lens(relevant_gems, lens_cost)


def prime_regrading_lens(prices):
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    relevant_gems = [
        gem
        for gem in gems
        if "Support" not in gem["name"]
        if not "wakened" in gem["name"]
        if gem["sparkline"]["data"]
        if not gem.get("corrupted")
        if gem["variant"] == "1"
    ]
    lens_cost = prices["Prime Regrading Lens"][0]["chaosValue"]
    return regrading_lens(relevant_gems, lens_cost)


def regrading_lens(relevant_gems, regrading_lens_cost):
    df = pd.DataFrame(relevant_gems)
    df["quality"] = (
            df.name.str.startswith("Anomalous")
            | df.name.str.startswith("Divergent")
            | df.name.str.startswith("Phantasmal")
    )
    df.loc[df.quality == False, "quality"] = "Superior"
    df.loc[df.quality == True, "quality"] = (
        df[df.quality == True].name.str.split().str[0]
    )
    df["basegem"] = (
        df.name.str.replace("Anomalous", "")
        .str.replace("Divergent", "")
        .str.replace("Phantasmal", "")
        .str.strip()
    )
    df = df.set_index(["quality", "basegem"])
    if 'gemQuality' in df.columns:
        df = df.drop('gemQuality', axis=1)
    df = df.dropna()
    gems = df
    df = pd.read_csv(f"{Path(__file__).resolve().parent}/gem_quality.csv")
    qual_weight_map = (
        df.drop_duplicates(keep="first").set_index(["Type", "Item"]).fillna(0)["Weight"]
    )
    qual_weight_map.head()
    gems["weight"] = qual_weight_map
    inter = (
        gems.reset_index()
        .groupby(["basegem"])
        .apply(
            lambda x: (
                x.set_index("quality")["chaosValue"].to_dict(),
                x.set_index("quality")["weight"].to_dict(),
            )
        )
    )
    result = pd.concat(
        [r for r in
         inter.apply(lambda x: markov_adps(x[1], x[0], regrading_lens_cost) if len(x[1]) > 1 else pd.Series())],
        keys=inter.index,
    )
    result = result.fillna(0)
    result = result.rename_axis(["basegem", "from"]).reset_index()
    result["value"] = result[["Anomalous", "Divergent", "Phantasmal"]].max(axis=1)
    result["to"] = result.apply(
        lambda x: "Anomalous"
        if x.value == x.Anomalous
        else "Divergent"
        if x.value == x.Divergent
        else "Phantasmal",
        axis=1,
    )
    result["actionable"] = result["from"] != result["to"]
    endresult = result.sort_values(["actionable", "value"], ascending=False).query(
        "actionable == True and value>0"
    )
    return endresult[["from", "basegem", "to", "value"]]


if __name__ == "__main__":
    pd.options.display.width = 0

    # print(pd.concat([secondary_regrading_lens(prices),prime_regrading_lens(prices)],ignore_index=True).sort_values('value',ascending=False))
    prices = retrieve_prices(["SkillGem", "Currency"])
    domain_result = pd.concat(
        [secondary_regrading_lens(prices), prime_regrading_lens(prices)],
        ignore_index=True,
    ).sort_values("value", ascending=False)
    result = {"result": list(domain_result.T.to_dict().values())}
    pprint(result)
