import datetime
import time
from itertools import combinations

import pandas as pd
import requests

from constants import ssid

import logging
logger = logging.getLogger(__name__)
def ask_for_exchange_rate(pay, get):
    try:
        return _ask_for_exchange_rate(pay,get)
    except requests.HTTPError:
        sleeping_time=100
        print(f'Sleeping for {sleeping_time} seconds because too many requests')
        time.sleep(sleeping_time)
        return _ask_for_exchange_rate(pay,get)
def _ask_for_exchange_rate(pay, get):
    print(f'Looking for {pay},{get}')
    headers = {
        "authority": "www.pathofexile.com",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "accept": "*/*",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
        "content-type": "application/json",
        "origin": "https://www.pathofexile.com",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://www.pathofexile.com/trade/exchange/Delirium",
        "accept-language": "en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7",
        "cookie": f"__cfduid=d5a027654f74766fc8b3dc0c2376afedd1585489737; POESESSID={ssid};"
        f" _ga=GA1.2.677066925.1585507944; stored_data=1; _gid=GA1.2.162826029.1587457745",
    }

    data = {"exchange": {"status": {"option": "online"}, "have": [pay], "want": [get]}}
    response = requests.post("https://www.pathofexile.com/api/trade/exchange/Delirium", headers=headers, json=data)
    rules = response.headers['X-Rate-Limit-Rules'].split(',')
    for rule in rules:
        limits =  response.headers[f"X-Rate-Limit-{rule}"].split(',')
        state =  response.headers[f"X-Rate-Limit-{rule}-State"].split(',')
        for limit,state in zip(limits,state):
            allowed, _, __ = [int(d) for d in limit.split(":")]
            current, window, __ = [int(d) for d in state.split(":")]
            if allowed - current < 2:
                print("Throttling")
                time.sleep(window / 2)
    response.raise_for_status()
    headers = {
        "authority": "www.pathofexile.com",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": f'https://www.pathofexile.com/trade/exchange/Delirium/{response.json()["id"]}',
        "accept-language": "en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7",
        "cookie": f"__cfduid=d5a027654f74766fc8b3dc0c2376afedd1585489737; POESESSID={ssid}; _ga=GA1.2.677066925.1585507944; stored_data=1; _gid=GA1.2.162826029.1587457745",
    }

    params = (
        ("query", response.json()["id"]),
        ("exchange", ""),
    )
    time.sleep(0.2)
    timestamp = pd.Timestamp.now()
    response = requests.get(
        f'https://www.pathofexile.com/api/trade/fetch/{",".join(response.json()["result"][:20])}',
        headers=headers,
        params=params,
    )
    rules = response.headers['X-Rate-Limit-Rules'].split(',')
    for rule in rules:
        limits = response.headers[f"X-Rate-Limit-{rule}"].split(',')
        state = response.headers[f"X-Rate-Limit-{rule}-State"].split(',')
        for limit, state in zip(limits, state):
            allowed, _, __ = [int(d) for d in limit.split(":")]
            current, window, __ = [int(d) for d in state.split(":")]
            if allowed - current < 2:
                print("Throttling")
                time.sleep(window / 2)
    response.raise_for_status()
    try:
        df = pd.DataFrame(
            [
                {
                    "pay_currency": result["listing"]["price"]["exchange"]["currency"],
                    "get_currency": result["listing"]["price"]["item"]["currency"],
                    "price": result["listing"]["price"]["exchange"]["amount"]
                    / result["listing"]["price"]["item"]["amount"],
                    "stock": result["listing"]["price"]["item"]["stock"],
                    "id": result["id"],
                }
                for result in response.json()["result"]
            ]
        )
        df["timestamp"] = timestamp
        return df
    except Exception as e:
        logger.exception('something went wrong')
        return pd.DataFrame()


def double_trouble(a, b):
    return pd.concat([ask_for_exchange_rate(a, b), ask_for_exchange_rate(b, a)], ignore_index=True)
class History():
    def __init__(self):
        self.state = pd.DataFrame()
    def update(self,new):
        self.state=pd.concat([self.state,new],ignore_index=True).set_index('id')
    def price(self):
        return self.state.groupby('id')

if __name__ == "__main__":
    currencies = [
        "chaos",
        "exa",
        'divine',
        'alch',
        'fuse',
        'alt',
        # 'regal',
        'vaal'
    ]
    for i in range(400):
        now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%s')
        start=time.time()
        print(f"Starting iteration {i}")
        pd.concat([double_trouble(a, b) for a, b in combinations(currencies, 2)]).to_parquet(f'market_depth/{now}.pq',allow_truncated_timestamps=True)
        end=time.time()
        sleeping_time = max(60-(end-start),0)
        print(f"Finished iteration {i}, sleeping for {sleeping_time} seconds")
        time.sleep(sleeping_time)
