import asyncio
import webbrowser

import requests

from tracker import track_all


def find_doryiani(seed: int):
    headers = {
        "authority": "www.pathofexile.com",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "accept": "*/*",
        "origin": "https://www.pathofexile.com",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        "dnt": "1",
        "content-type": "application/json",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "referer": "https://www.pathofexile.com/trade/search/Metamorph",
        "accept-encoding": "gzip, deflate",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,pl;q=0.5,sl;q=0.4",
        "cookie": "__cfduid=dd651caa097eb331c57261f6efc584cad1573913545; _ga=GA1.2.1737961421.1574104651; stored_data=1; POESESSID=f60d15f538a00373a2557e0532191bc1; _gid=GA1.2.788587831.1579890301",
    }
    data = {
        "query": {
            "status": {"option": "online"},
            "stats": [
                {
                    "type": "and",
                    "filters": [
                        {
                            "id": "explicit.pseudo_timeless_jewel_doryani",
                            "value": {"min": seed, "max": seed},
                            "disabled": False,
                        }
                    ],
                }
            ],
        },
        "sort": {"price": "asc"},
    }
    response = requests.post("https://www.pathofexile.com/api/trade/search/Metamorph", headers=headers, json=data)
    # if response.json()['result']:
    hash = response.json()['id']
    return hash

seeds=[
7473,
4881,
4886,
3442,
6697,
6847,
5071,
4410,
4432,
7000,
6932,
7800,
6260,
658,
3828,
4481,
6872,
6650,
    288,
    1167,
    6650,
    6018,
    4913,
    5831,
    4481,
    5454,
    1737,
    1910,
    3828,
    6260,
    6650,
    5296,
    2671,
    3624,
    453,
    2435,
    1850,
    1448,
    4665,
    5494,
    6753,
    6998,
    1389,
    408,
    4556,
    137,
    1423,
    1492,
    4296,
    6543,
    2569,
    4718,
    2501,

]+[751,5977,4410,6677,4959,]
zerphi=[
    6697,

]
xibaqua=[
    362,4794,5806,5637,5806,4913,5799,1525
]
hashes =[find_doryiani(seed) for seed in seeds]
print(hashes)
asyncio.get_event_loop().run_until_complete(track_all(*hashes))
