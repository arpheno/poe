import pandas as pd

from poe.ninja import retrieve_prices


def vaal_gems(prices):
    gems = [
        item
        for price in prices.values()
        for item in price
        if item["type"] == "SkillGem"
    ]
    df = pd.DataFrame(gems)
    assign_types = (
        lambda x: "special"
        if any(
            y in x for y in ("Enhance Support", "Enlighten Support", "Empower Support")
        )
        else "Awakened"
        if "Awakened" in x
        else "alt"
        if any(y in x for y in ("nomalous", "ivergent", "hantasmal"))
        else "normal"
    )
    funcs = {
        "special": lambda row: row["4c"] * (1 / 8)
        + row["2c"] * (1 / 8)
        + row["3c"] * 6 / 8
        - row["3"],
        "Awakened": lambda row: row["6c"] * (1 / 8)
        + row["4c"] * (1 / 8)
        + row.get("5c", 0) * 6 / 8
        - row.get("5", 1000),
        "normal": lambda row: row["21c"] * (1 / 8)
        + row.get("19c", 0) * (1 / 8)
        + row["20c"] * 6 / 8
        - row["20"],
        "alt": lambda row: row["21/20c"] * (1 / 8)
        + row.get("19/20c", row.get("20/20c", 0)) * (1 / 8)
        + row.get("20/23c", 0) * (18 / 20) * (1 / 8)
        + row.get("20/17c", row.get("20c", 0)) * (1 / 8)
        + row["20/20c"] * 4 / 8
        - row.get("20/20", 10000),
    }

    def map_to_value(row):
        return funcs[assign_types(row.name)](row)

    pivoted_gems = df.pivot(index="name", columns="variant", values="chaosValue")
    domain_result = (
        pivoted_gems.apply(map_to_value, axis=1)
        .sort_values(ascending=False)
        .reset_index()
    )
    domain_result.columns = ["name", "profit"]
    domain_result = domain_result.dropna()
    return domain_result


if __name__ == "__main__":
    prices = retrieve_prices(["SkillGem"])
    vaal_gems(prices)
