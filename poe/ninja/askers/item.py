from collections import defaultdict

import requests


def ask_ninja_item(type, league="Scourge"):
    url="https://poe.ninja/api/data/itemoverview"
    params = dict(type=type, league=league)
    response = requests.get(url=url, params=params)
    print(url,type,response.status_code)
    data = response.json()
    for c in data['lines']:
        if not c.get('name'):
            c['name']=c['currencyTypeName']
            c['chaosValue']=c["receive"]["value"]
        c['type']=type
    return_value = defaultdict(list)
    for c in data['lines']:
        return_value[c['name']].append(c)
    return dict(return_value)