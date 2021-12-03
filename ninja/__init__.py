from collections import ChainMap

import pandas as pd

import requests

from ninja.askers.facade import asker


def retrieve_currency_rates():
    items = [
        "Fragment",
        "Currency",
        "Scarab",
        "Oil",
        "Fossil",
        "Resonator",
        "Prophecy",
        "Incubator",
        "UniqueMap",
        "UniqueJewel",
        "UniqueFlask",
        "UniqueArmour",
        "UniqueWeapon",
        "UniqueAccessory",
        "Essence",
        "DeliriumOrb",
        "DivinationCard",
        "Map",
        "SkillGem",
        "BaseType",
    ]
    rates = [asker(curr) for curr in items]
    return ChainMap(*[rate for rate in rates])


key_builders = {""}


class DefaultBuilder:
    def __call__(self, item):
        pass


def key_builder_factory(type):
    return key_builders.get("type", DefaultBuilder())


def lookup_key(item):
    return ()


def _currencyreport(url, type, league="Scourge"):
    params = dict(type=type, league=league)
    response = requests.get(url=url, params=params)
    print(url, type, response.status_code)
    data = response.json()
    lines = [line for line in data["lines"] if "pay" in line if "receive" in line]
    first = [pd.Series(c["receive"]) for c in lines]
    second = [pd.Series(c["pay"]) for c in lines]
    result = pd.concat(first + second, axis=1).T
    currency_details = pd.DataFrame(data["currencyDetails"]).set_index("id")["name"]
    result["pay_currency"] = result["pay_currency_id"].map(currency_details)
    result["get_currency"] = result["get_currency_id"].map(currency_details)
    return result


def currencyreport():
    currs = ["Fragment", "Currency"]
    # currs = ["Currency"]
    rates = pd.concat(
        [
            _currencyreport(
                "https://poe.ninja/api/data/currencyoverview",
                curr,
            )
            for curr in currs
        ]
    )
    return rates.dropna()


def refine_report(cr):
    cr["receive"] = cr["pay_currency"] == "Chaos Orb"
    cr["sample_time_utc"] = pd.to_datetime(cr["sample_time_utc"])
    cr["value"] = cr["value"].astype("float64")
    cr.loc[cr.pay_currency != "Chaos Orb", "value"] = 1 / cr.loc[cr.pay_currency != "Chaos Orb", "value"]
    cr.loc[cr.pay_currency != "Chaos Orb", "get_currency"] = cr[cr.pay_currency != "Chaos Orb"]["pay_currency"]
    cr.loc[cr.pay_currency != "Chaos Orb", "pay_currency"] = "Chaos Orb"
    return cr


if __name__ == "__main__":
    a = currencyreport()
    ask_ninja(
        "https://poe.ninja/api/data/currencyoverview",
        "Currency",
    )
