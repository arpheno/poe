from collections import defaultdict

import requests


def ask_ninja_curr(type, league="Scourge"):
    url = "https://poe.ninja/api/data/currencyoverview"
    params = dict(type=type, league=league)
    response = requests.get(url=url, params=params)
    data = response.json()
    print('.',end='')
    for c in data["lines"]:
        c["name"] = c["currencyTypeName"]
        c["chaosValue"] = c["receive"]["value"]
        c["type"] = type
    return_value = defaultdict(list)
    for c in data["lines"]:
        return_value[c["name"]].append(c)
    return dict(return_value)


if __name__ == "__main__":
    ask_ninja_curr("Fragment", league="Scourge")
