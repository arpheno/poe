from pprint import pprint

import requests

from poe import headers

data = {
    "query": {
        "status": {"option": "any"},
        "stats": [{"type": "and", "filters": []}],
        "filters": {
            "trade_filters": {"filters": {"account": {"input": "swozn"}, "sale_type": {"option": "any"}}},
            "map_filters": {"filters": {"map_tier": {"min": 1}}},
        },
    },
    "sort": {"price": "asc"},
}
payload="".join(str(data).split()).replace("'",'"')
response = requests.post('https://www.pathofexile.com/api/trade/search/Ultimatum', headers=headers, data=payload)

response_data = response.json()
print(response_data)
url = f"https://www.pathofexile.com/api/trade/fetch/{','.join(response_data['result'][:10])}?query={response_data['id']}"
print(url)
response = requests.get(url, headers=headers)
pprint(response.json())
