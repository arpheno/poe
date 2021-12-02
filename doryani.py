import asyncio
import webbrowser

import requests

from tracker import track_all
from constants import ssid
import time
def find_doryiani(seed: int,name_of='doryani'):
    cookies = {
        'cf_clearance': '7d322aa725fafce9ef1ebc8a26759033b127dd7f-1618777267-0-150',
        '_ga': 'GA1.2.1675387988.1618777334',
        'stored_data': '1',
        'POESESSID': '1477e79edd84ca2980fc97f5617b7234',
        '_gid': 'GA1.2.1879284383.1636797311',
    }
    headers = {
        'Pragma': 'no-cache',
        'Origin': 'https://www.pathofexile.com',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6,pl;q=0.5,sl;q=0.4',
        'Sec-WebSocket-Key': 'e5K704b5btGaJGoJ0Do+XA==',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36',
        'Upgrade': 'websocket',
        'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
        'Cache-Control': 'no-cache',
        'Connection': 'Upgrade',
        'Sec-WebSocket-Version': '13',
        'Cookie': '; '.join(f'{key}={value}' for key, value in cookies.items())
    }
    data = {
        "query": {
            "status": {"option": "online"},
            "stats": [
                {
                    "type": "and",
                    "filters": [
                        {
                            "id": f"explicit.pseudo_timeless_jewel_{name_of}",
                            "value": {"min": seed, "max": seed},
                            "disabled": False,
                        }
                    ],
                }
            ],
        },
        "sort": {"price": "asc"},
    }

    response = requests.post("https://www.pathofexile.com/api/trade/search/Scourge", headers=headers, json=data)
    # if response.json()['result']:
    if response.status_code == 429:
        print('too fast (')
    time.sleep(5)
    result = response.json()
    result_hash = result['id']
    if result['result']:
        print(f'https://www.pathofexile.com/trade/search/Scourge/{result_hash}')
    return result_hash
seeds=dict(
    balbala=[6870],
doryani=[
6150,
    7590,
    2854,
    6401,
    4319,
    2228,
    7112,
    3414,
    5531,
    5337,

],
xibaqua=[
    3773,
    243,
    7925,
    1569,
    6494,


],
ahuana = [
    4497,
    1419,
    485,
    5379,
    1539,
    4407,
    1110,
    3985,
    3334,


])
hashes=[]
for name_of,seeds in seeds.items():
    hashes +=[find_doryiani(seed,name_of) for seed in seeds[:6]]
    print(hashes)
print(hashes)
asyncio.get_event_loop().run_until_complete(track_all(*hashes))
