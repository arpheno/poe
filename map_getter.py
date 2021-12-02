from pprint import pprint

import requests
import requests

headers = {
    'authority': 'www.pathofexile.com',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'accept': '*/*',
    'dnt': '1',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'content-type': 'application/json',
    'origin': 'https://www.pathofexile.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.pathofexile.com/trade/search/Ultimatum',
    'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,pl;q=0.5,sl;q=0.4',
    'cookie': 'cf_clearance=7d322aa725fafce9ef1ebc8a26759033b127dd7f-1618777267-0-150; _ga=GA1.2.1675387988.1618777334; stored_data=1; POESESSID=93e8b04dcc926d271d3e2ca9a5ef07dd',
}


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
