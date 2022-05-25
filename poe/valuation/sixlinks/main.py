import pandas as pd

from poe.ninja import retrieve_prices


def sixlink(prices):
    body_armours = {
        key: sorted(value, key=lambda x: x.get("chaosValue"))
        for key, value in prices.items()
        if value[0].get("itemType") == "Body Armour"
        if value[0].get("type") == "UniqueArmour"
    }
    operating_cost = 350 * prices["Jeweller's Orb"][0].get(
        "chaosValue", 1000
    ) + 1500 * (1 - 0.2) * prices["Orb of Fusing"][0].get("chaosValue", 1000)
    six_link_income = {
        key: {
            "profit": value[-1]["chaosValue"] - value[0]["chaosValue"] - operating_cost,
            "nmv": value[-1]["chaosValue"] - value[0]["chaosValue"],
            "cogs": value[0]["chaosValue"],
            "cost": value[0]["chaosValue"] + operating_cost,
            "relative_profit": (
                value[-1]["chaosValue"] - value[0]["chaosValue"] - operating_cost
            )
            / (value[0]["chaosValue"] + operating_cost),
        }
        for key, value in body_armours.items()
    }
    return pd.DataFrame(six_link_income).T.sort_values("profit", ascending=False)


if __name__ == "__main__":
    prices = retrieve_prices()

    valuations = sixlink(prices)
    print(valuations)
