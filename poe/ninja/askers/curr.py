from collections import defaultdict

import requests

from poe.constants import LEAGUE
from poe.ninja.askers.models import CurrencyReply


def ask_ninja_curr(type, league=LEAGUE):
    data = raw_ninja_currency_reply(type, league)

    print(".", end="")
    for c in data["lines"]:
        c["name"] = c["currencyTypeName"]
        c["chaosValue"] = c.get("receive", {"value": 0})["value"]
        c["type"] = type
    return_value = defaultdict(list)
    for c in data["lines"]:
        return_value[c["name"]].append(c)
    return dict(return_value)


def raw_ninja_currency_reply(type, league=LEAGUE):
    url = "https://poe.ninja/api/data/currencyoverview"
    params = dict(type=type, league=league)
    response = requests.get(url=url, params=params)
    data = response.json()
    return data


if __name__ == "__main__":
    data = raw_ninja_currency_reply("Currency")
    model = CurrencyReply(**data)
    print(model)
