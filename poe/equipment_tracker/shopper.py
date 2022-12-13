# WS client example

import asyncio
import json
from asyncio import sleep
from pprint import pprint
from typing import Callable

import aiohttp
import requests
import websockets

from constants import ssid, LEAGUE

headers = {
    "Origin": "https://www.pathofexile.com",
    "Cookie": f"POESESSID={ssid}",
    "User-Agent": "Mozilla/5.011 Macintosh",
}

extra_headers = list(headers.items())
pprint(extra_headers)


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


class Tracker:
    def __init__(self, callback: Callable):
        self.callback = callback
        self.websocket_opts = dict(
            ssl=True,
            extra_headers=extra_headers,
            close_timeout=10,
            ping_interval=10000,
            ping_timeout=10000,
        )

    async def handle_search_request(self, hash: str):
        uri = f"wss://www.pathofexile.com/api/trade/live/{LEAGUE}/{hash}"
        print(f"tracking {hash}")
        details_page= f"https://www.pathofexile.com/api/trade/fetch/{result}"
        async with aiohttp.ClientSession(headers=headers) as session:
            async with websockets.connect(uri=uri,**self.websocket_opts) as websocket:
                while True:
                    data = await websocket.recv()
                    if "auth" in data:
                        continue
                    for result in json.loads(data)["new"]:
                        html = await fetch(
                            session, details_page
                        )
                        data = json.loads(html)["result"][0]
                        #some business logic
                        return data

                        print(data)
                        #self.callback(data)


def direct_whisper(token):
    url = 'https://www.pathofexile.com/api/trade/whisper'
    response = requests.post(url, json=dict(token=token), headers={'x-requested-with': 'XMLHttpRequest', **headers})
    return response.json()


def whisper_seller(data):
    direct_whisper(data['listing']['whisper_token'])


async def make_shopper(hash):
    behaviour = whisper_seller
    buyer = Tracker(behaviour)
    result = await buyer.handle_search_request(hash)
    business_logic(data)
    pass


async def shop(hash):
    shopper = asyncio.create_task(make_shopper(hash))
    await sleep(5)
    await shopper


import asyncio

if __name__ == "__main__":
    hashes = ["Kjjo6pgC5"]
    # for name_of, seeds in seeds.items():
    #     hashes += [find_doryiani(seed, name_of) for seed in seeds[:6]]
    #     print(hashes)
    print(hashes)
    asyncio.get_event_loop().run_until_complete(shop(hashes[0]))
